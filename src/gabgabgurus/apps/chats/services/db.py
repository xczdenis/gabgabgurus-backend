from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from gabgabgurus.apps.chats.enums import ChannelTypes, MessageStatuses
from gabgabgurus.apps.chats.models import Channel, Message, MessageStatus, UserChannel
from gabgabgurus.apps.chats.selectors import (
    get_channel_members,
    get_channels_by_participants,
    get_undelivered_messages,
)
from gabgabgurus.common.decorators import default
from gabgabgurus.common.utils.models import bulk_create, save
from gabgabgurus.config import app_config
from gabgabgurus.config.exceptions import EntityDoesntExist, Forbidden, NotRequiredContent

User = get_user_model()


@default(channel_id=None, sender=None)
def create_message(**kwargs) -> Message:
    channel_id = kwargs["channel_id"]
    sender = kwargs["sender"]

    if not channel_id:
        raise NotRequiredContent("Channel is required")
    if not sender:
        raise NotRequiredContent("Sender is required")

    channel = Channel.objects.filter(id=channel_id).first()
    if not channel:
        raise EntityDoesntExist(f"Channel with id {channel_id} not found")

    if not channel.is_available_for_user(sender):
        raise Forbidden("This channel is not available for user")

    message = Message(**kwargs)
    message = save(message)

    return message


def create_message_statuses_for_recipients(
    message: Message, sender: User, status: MessageStatuses | None = None
):
    recipients = get_channel_members(message.channel, sender)
    return message.create_message_statuses(recipients, status)


def filter_channels_queryset(
    queryset: QuerySet[Channel | UserChannel],
    related_field: str = "",
    participants: list[str | int | User] | None = None,
    participant_slug_field: str = "",
    channel_type: ChannelTypes | None = None,
) -> QuerySet[UserChannel]:
    """
    Filter a queryset of Channel or UserChannel based on participants and channel type.

    This function allows for filtering a queryset by matching participants and/or channel type.
    It can handle related fields and custom participant identifier fields (slugs).

    :param queryset: The initial queryset to be filtered.
    :param related_field: The name of the related field to filter through (if any).
    :param participants: A list of participants to filter by. Can be any strings, IDs, or User objects.
    :param participant_slug_field: The field on the participant to filter by (e.g., 'email').
    :param channel_type: The type of channel to filter by (if filtering by channel type is desired).
    :return: A queryset of UserChannel that matches the filters.
    """

    def make_filter_key(filtered_field: str, related: str, slug: str = ""):
        _filter_key = filtered_field
        if related:
            _filter_key = f"{related}__{_filter_key}"
        if slug:
            _filter_key += f"__{slug}"
        return _filter_key

    if participants is not None:
        filter_key = make_filter_key("participants", related_field, participant_slug_field)
        for participant in participants:
            queryset = queryset.filter(**{filter_key: participant})

    if channel_type is not None:
        filter_key = make_filter_key("channel_type", related_field)
        queryset = queryset.filter(**{filter_key: channel_type})

    return queryset.all()


def init_private_dialog(owner: User, participant_ids: list[int]):
    """
    Initialize a private dialog channel between the owner and the specified participants.

    This function checks if a private channel already exists with the given participants.
    If it does not exist, it creates a new private channel and adds the users to it.

    :param owner: The User object representing the owner of the dialog.
    :param participant_ids: A list of user IDs for those who will participate in the dialog.
    :return: The Channel object representing the private dialog.
    """

    channel_type = ChannelTypes.PRIVATE
    member_ids = [owner.id, *participant_ids]

    channel = get_channels_by_participants(
        participants=member_ids,
        channel_type=channel_type,
        related=False,
        add_participants=False,
    ).first()

    if channel is None:
        channel = create_channel(owner=owner, channel_type=channel_type)

    create_user_channels(member_ids, channel)

    return channel


@default(owner=None, channel_type=ChannelTypes.PRIVATE)
def create_channel(**kwargs) -> Channel:
    """
    Create a new channel without checking if that one with given parameters already exists or not.

    :param kwargs:
    :return:
    """
    owner = kwargs["owner"]
    if not owner:
        raise NotRequiredContent("The owner must be provided when creating a channel")
    new_channel = Channel(**kwargs)
    save(new_channel)
    return new_channel


def create_user_channels(user_ids: list[int], channel: Channel) -> QuerySet[User]:
    not_in_channel_users = User.objects.filter(id__in=user_ids).exclude(user_channels__channel=channel)
    user_channel_objects = (UserChannel(user=user, channel=channel) for user in not_in_channel_users)
    return bulk_create(UserChannel, user_channel_objects)


@default(batch_size=app_config.BATCH_SIZE_FOR_BULK_ACTION, message_status=MessageStatuses.DELIVERED)
def deliver_messages(user: User, channel: Channel | int | None = None, **kwargs) -> QuerySet[Message]:
    batch_size = kwargs["batch_size"]
    message_status = kwargs["message_status"]

    undelivered_messages = get_undelivered_messages(user, channel, related=False)

    message_status_objects = (
        MessageStatus(user=user, message=message, status=message_status) for message in undelivered_messages
    )

    MessageStatus.objects.bulk_create(message_status_objects, batch_size)
    bulk_create(MessageStatus, message_status_objects, **kwargs)

    return undelivered_messages


def mark_messages_as_read(message_ids: list[int], recipient_id: int):
    MessageStatus.objects.filter(
        message_id__in=message_ids,
        user_id=recipient_id,
    ).update(status=MessageStatuses.READ)
