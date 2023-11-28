from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Exists, OuterRef, Q, QuerySet
from django.db.models.functions import Length

from gabgabgurus.apps.hobbies.models import Hobby
from gabgabgurus.apps.languages.models import Country, Language
from gabgabgurus.apps.user_details.selectors import add_languages_to_user_queryset
from gabgabgurus.apps.users.services import make_cache_key_user_last_activity
from gabgabgurus.common.decorators import default

User = get_user_model()


@default(with_relations=True)
def get_top_users(top_users_count: int, **kwargs):
    users_qs = get_users(with_relations=kwargs["with_relations"])

    users_qs = users_qs.annotate(about_me_short=Length("about_me"))

    filter_avatar = ~Q(avatar="")
    filter_about_me = Q(about_me_short__gt=30)

    users_qs = users_qs.filter(filter_avatar, filter_about_me)
    users_qs = users_qs.order_by("-date_joined")[:top_users_count]
    return users_qs


def get_users(
    speaks: list[Language | int | str] | None = None,
    speaks_lookup: str = "",
    learning: list[Language | int | str] | None = None,
    learning_lookup: str = "",
    countries: list[Country | int | str] | None = None,
    countries_lookup: str = "",
    hobbies: list[Hobby | int | str] | None = None,
    hobbies_lookup: str = "",
    with_relations: bool = True,
    blocker: User | None = None,
) -> QuerySet[User]:
    """
    Fetches a QuerySet of User objects filtered by languages spoken, languages learning, countries,
    and hobbies.

    This function can further refine these filters using lookup fields. It also allows for the option
    to include related data and to annotate the queryset with a blocker's status.

    :param speaks: Languages the user should speak.
    :param speaks_lookup: Field lookup for 'speaks' filter.
    :param learning: Languages the user is learning.
    :param learning_lookup: Field lookup for 'learning' filter.
    :param countries: Countries associated with the user.
    :param countries_lookup: Field lookup for 'countries' filter.
    :param hobbies: Hobbies the user is interested in.
    :param hobbies_lookup: Field lookup for 'hobbies' filter.
    :param with_relations: Whether to prefetch related objects.
    :param blocker: The User object to check for blocking status.

    :return: A QuerySet of User objects.
    """

    users_qs = User.objects

    def make_filter_key(related_name, lookup_field):
        filter_key = "{}__in".format(related_name)
        if lookup_field:
            filter_key = "{}__{}__in".format(related_name, lookup_field or "")
        return filter_key

    def add_filter(field_name, lookup_field, filter_value):
        if filter_value:
            filter_key = make_filter_key(field_name, lookup_field)
            return users_qs.filter(**{filter_key: filter_value})
        return users_qs

    if speaks is not None:
        language_filter_key = make_filter_key("user_languages__language", speaks_lookup)
        users_qs = users_qs.filter(
            **{language_filter_key: speaks},
            user_languages__is_speaking=True,
        )
    if learning is not None:
        language_filter_key = make_filter_key("user_languages__language", learning_lookup)
        users_qs = users_qs.filter(
            **{language_filter_key: speaks},
            user_languages__is_speaking=True,
        )

    users_qs = add_filter("country", countries_lookup, countries)
    users_qs = add_filter("hobbies", hobbies_lookup, hobbies)

    if blocker:
        users_qs = add_is_blocked(users_qs, blocker)

    if with_relations:
        users_qs = annotate_user_queryset_with_relations(users_qs)

    users_qs = users_qs.order_by("-id")
    users_qs = users_qs.distinct()

    return users_qs.all()


@default(
    hobbies=True,
    country=True,
    all_languages=False,
    languages_by_type=True,
    blocker=None,
)
def annotate_user_queryset_with_relations(user_qs: QuerySet[User], **kwargs) -> QuerySet[User]:
    updated_qs = user_qs

    updated_qs = add_languages_to_user_queryset(
        updated_qs,
        all=kwargs["all_languages"],
        by_type=kwargs["languages_by_type"],
    )

    if kwargs["hobbies"]:
        updated_qs = updated_qs.prefetch_related("hobbies")

    if kwargs["country"]:
        updated_qs = updated_qs.select_related("country")

    blocker = kwargs["blocker"]
    if blocker is not None:
        updated_qs = add_is_blocked(updated_qs, blocker)

    return updated_qs


def add_is_blocked(queryset: QuerySet, blocker: User, out_ref_lookup_field: str = "pk") -> QuerySet:
    """
    Annotates a queryset with a boolean field "is_blocked" indicating if each user has been blocked
    by the given user.

    This function uses a subquery to check if the users in the provided queryset have been blocked by
    the 'blocker' user. It annotates the given queryset with the boolean field 'is_blocked'

    :param queryset: The queryset of User objects to annotate.
    :param blocker: The User object representing the blocker.
    :param out_ref_lookup_field: The field in User model to refer to for the outer reference.

    :return: The annotated queryset with the 'is_blocked' boolean field.
    """
    is_blocked_subquery = User.objects.filter(id=blocker.id, blocked_users=OuterRef(out_ref_lookup_field))
    queryset = queryset.annotate(is_blocked=Exists(is_blocked_subquery))

    blocked_for_blocker_subquery = User.objects.filter(
        id=OuterRef(out_ref_lookup_field), blocked_users=blocker
    )
    queryset = queryset.annotate(blocked_for=Exists(blocked_for_blocker_subquery))
    return queryset


def get_user_last_activity_timestamp_from_cache(user: User):
    last_activity = get_user_last_activity_from_cache(user.id)

    if last_activity is None and user.last_login is not None:
        last_activity = user.last_login

    if last_activity is not None:
        last_activity = last_activity.timestamp()

    return last_activity


def get_user_last_activity_from_cache(user_id: int):
    cache_key = make_cache_key_user_last_activity(user_id)
    return cache.get(cache_key)
