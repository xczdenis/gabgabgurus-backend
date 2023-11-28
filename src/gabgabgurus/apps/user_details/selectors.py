from django.contrib.auth import get_user_model
from django.db.models import Prefetch, QuerySet

from gabgabgurus.apps.languages.enums import LanguageTypes
from gabgabgurus.apps.user_details.models import UserLanguage
from gabgabgurus.common.decorators import default

User = get_user_model()


@default(language=True, user=False)
def annotate_user_languages_with_relations(
    user_languages_qs: QuerySet[UserLanguage], **kwargs
) -> QuerySet[UserLanguage]:
    updated_qs = user_languages_qs

    if kwargs["language"]:
        updated_qs = updated_qs.select_related("language")

    if kwargs["user"]:
        updated_qs = updated_qs.select_related("user")

    return updated_qs


@default(all=True, by_type=False)
def add_languages_to_user_queryset(user_qs: QuerySet[User], **kwargs):
    updated_qs = user_qs
    lookup = "user_languages"
    user_languages = get_user_languages()

    if kwargs.get("all"):
        prefetch = Prefetch(lookup, queryset=user_languages)
        updated_qs = updated_qs.prefetch_related(prefetch)

    if kwargs.get("by_type"):
        prefetch = Prefetch(
            lookup,
            queryset=user_languages.filter(is_speaking=True),
            to_attr=LanguageTypes.SPEAKS.value,
        )
        updated_qs = updated_qs.prefetch_related(prefetch)

        prefetch = Prefetch(
            lookup,
            queryset=user_languages.filter(is_learning=True),
            to_attr=LanguageTypes.LEARNING.value,
        )
        updated_qs = updated_qs.prefetch_related(prefetch)

    return updated_qs


def get_user_languages(with_related: bool = True) -> QuerySet[UserLanguage]:
    qs = UserLanguage.objects
    if with_related:
        qs = qs.select_related("language")
    return qs
