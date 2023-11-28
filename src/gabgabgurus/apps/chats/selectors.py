from django.contrib.auth import get_user_model
from django.db.models import (
    BooleanField,
    Case,
    Max,
    Min,
    OuterRef,
    PositiveSmallIntegerField,
    Prefetch,
    Q,
    QuerySet,
    Subquery,
    Sum,
    Value,
    When,
)

from gabgabgurus.apps.chats.enums import MessageStatuses
from gabgabgurus.apps.chats.models import Channel, Message, MessageStatus, UserChannel
from gabgabgurus.apps.users.selectors import add_is_blocked
from gabgabgurus.common.decorators import default

User = get_user_model()


@default(
    slug_field="id",
    channel_type=None,
    related=True,
    add_participants=True,
    blocker=None,
)
def get_channels_by_participants(participants: list[str | int | User], **kwargs) -> QuerySet[UserChannel]:
    qs = get_channels(**kwargs)

    filter_key = f"participants__{kwargs['slug_field']}"
    for participant in participants:
        qs = qs.filter(**{filter_key: participant})

    if kwargs["channel_type"] is not None:
        qs = qs.filter(channel_type=kwargs["channel_type"])

    return qs.all()


@default(related=True, add_participants=True, blocker=None)
def get_channels(owner: User | None = None, **kwargs) -> QuerySet[Channel]:
    qs = Channel.objects

    if owner:
        qs = qs.filter(owner=owner)

    if kwargs["related"]:
        qs = qs.select_related("owner")

    if kwargs["add_participants"]:
        qs = add_participants(qs, **kwargs)

    return qs.all()


@default(
    related=True,
    add_participants=True,
    add_last_message=True,
    metadata=True,
    exclude_user_from_participants=True,
)
def get_user_channels(user: User | None = None, **kwargs) -> QuerySet[UserChannel]:
    qs = UserChannel.objects

    if user:
        qs = qs.filter(user=user)

    if kwargs["related"]:
        qs = qs.select_related("channel__owner", "user")

    if kwargs["add_participants"]:
        qs = add_participants(
            qs,
            lookup_field="channel__participants",
            participants_qs=User.objects.exclude(id=user.id),
            blocker=user,
        )

    if kwargs["add_last_message"]:
        qs = add_last_message_to_user_channels(qs)

    if kwargs["metadata"]:
        qs = add_last_activity_to_user_channels(qs)
        qs = add_unread_count_to_user_channels(qs, user)

    qs = qs.distinct()
    qs = qs.order_by("-id")

    return qs.all()


@default(participants_qs=None, lookup_field="participants", blocker=None)
def add_participants(users_qs: QuerySet, **kwargs) -> QuerySet:
    participants_qs = kwargs["participants_qs"]
    if participants_qs is None:
        participants_qs = User.objects.all()

    blocker = kwargs["blocker"]
    if blocker:
        participants_qs = add_is_blocked(participants_qs, blocker)

    prefetch_participants = Prefetch(kwargs["lookup_field"], participants_qs)
    updated_queryset = users_qs.prefetch_related(prefetch_participants)
    return updated_queryset


def add_last_message_to_user_channels(user_channel_qs: QuerySet[UserChannel]) -> QuerySet[UserChannel]:
    last_messages = Message.objects.filter(channel=OuterRef("channel_id")).order_by("-created_at", "-id")
    subquery = Subquery(last_messages.values("text")[:1])
    user_channel_qs = user_channel_qs.annotate(last_message=subquery)
    return user_channel_qs


def add_last_activity_to_user_channels(user_channel_qs: QuerySet[UserChannel]) -> QuerySet[UserChannel]:
    user_channel_qs = user_channel_qs.annotate(last_activity=Max("channel__messages__updated_at"))
    return user_channel_qs


def add_unread_count_to_user_channels(
    user_channel_qs: QuerySet[UserChannel], user: User
) -> QuerySet[UserChannel]:
    when_condition = When(
        channel__messages__message_statuses__user=user,
        channel__messages__message_statuses__status=MessageStatuses.DELIVERED,
        then=1,
    )
    case = Case(when_condition, default=0, output_field=PositiveSmallIntegerField())
    return user_channel_qs.annotate(unread_count=Sum(case))


@default(related=True)
def get_undelivered_messages(user: User, channel: Channel | int | None = None, **kwargs) -> QuerySet[Message]:
    qs = get_user_channel_messages(user, channel, **kwargs)
    qs = qs.filter(~Q(sender=user))
    qs = add_is_delivered_to_messages(qs, user)
    qs = qs.filter(is_delivered=0)
    return qs.all()


@default(related=True, statuses=False)
def get_user_channel_messages(
    user: User, channel: Channel | int | None = None, **kwargs
) -> QuerySet[Message]:
    qs = get_messages(**kwargs)
    qs = qs.filter(channel__participants=user)

    if channel is not None:
        qs = qs.filter(channel=channel)

    return qs.all()


@default(related=True, statuses=False)
def get_messages(filters: dict | None = None, **kwargs) -> QuerySet[Message]:
    qs = Message.objects

    if kwargs["related"]:
        qs = qs.select_related("channel__owner", "sender")

    if kwargs["statuses"]:
        qs = add_statuses_to_messages(qs)

    if filters is not None:
        qs = qs.filter(**filters)

    qs = qs.order_by("-created_at", "-id")

    return qs.all()


def add_statuses_to_messages(messages_qs: QuerySet[Message]) -> QuerySet[Message]:
    message_statuses = (
        MessageStatus.objects.filter(message=OuterRef("id"))
        .exclude(user=OuterRef("sender_id"))
        .values("message")
        .annotate(min_status=Min("status"))
    )
    subquery = Subquery(message_statuses.values("min_status")[:1])
    messages_qs = messages_qs.annotate(status=subquery)

    return messages_qs


def add_is_mine_to_messages(messages_qs: QuerySet[Message], user: User) -> QuerySet[Message]:
    when_condition = When(sender=user, then=1)
    case = Case(when_condition, default=0, output_field=PositiveSmallIntegerField())
    return messages_qs.annotate(is_mine=Max(case))


def add_is_delivered_to_messages(messages_qs: QuerySet[Message], user: User) -> QuerySet[Message]:
    when_condition = When(message_statuses__user=user, then=1)
    case = Case(when_condition, default=0, output_field=PositiveSmallIntegerField())
    return messages_qs.annotate(is_delivered=Max(case))


def get_channel_members(channel: Channel | int, exclude_user: User | int | None = None) -> QuerySet[User]:
    channel_id = channel.id if isinstance(channel, Channel) else channel
    qs = Channel.objects.filter(id=channel_id).first().participants
    if exclude_user is not None:
        exclude_user_id = exclude_user.id if isinstance(exclude_user, User) else exclude_user
        qs = qs.exclude(id=exclude_user_id)
    return qs.all()


@default(related=True)
def get_unread_messages(recipient: User, **kwargs) -> QuerySet[MessageStatus]:
    message_statuses = get_message_statuses(**kwargs)
    message_statuses = message_statuses.filter(user=recipient).exclude(status=MessageStatuses.READ)
    return message_statuses


@default(related=True, add_is_read=False)
def get_message_statuses(**kwargs) -> QuerySet[MessageStatus]:
    qs = MessageStatus.objects

    if kwargs["related"]:
        qs = qs.select_related("user", "message", "message__channel", "message__sender")

    if kwargs["add_is_read"]:
        qs = add_is_read_to_message_statuses(qs)

    qs = qs.order_by("-created_at", "-id")

    return qs.all()


def add_is_read_to_message_statuses(qs: QuerySet[MessageStatus]) -> QuerySet[MessageStatus]:
    when_condition = When(status=MessageStatuses.READ, then=Value(True))
    case = Case(when_condition, default=Value(False), output_field=BooleanField())
    return qs.annotate(is_read=case)
