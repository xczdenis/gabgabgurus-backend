from gabgabgurus.api.v1.chats.enums import ChatMessageTypes
from gabgabgurus.api.v1.chats.serializers.messages import (
    MarkMessagesAsReadRequest,
    MessageRequest,
    MessageResponse,
)
from gabgabgurus.apps.chats.enums import MessageStatuses
from gabgabgurus.apps.chats.selectors import get_channel_members, get_messages
from gabgabgurus.apps.chats.services.cache import get_chat_connected_users
from gabgabgurus.apps.chats.services.db import (
    create_message,
    create_message_statuses_for_recipients,
    mark_messages_as_read,
)
from gabgabgurus.apps.users.services import make_user_notify_consumer_group_name
from gabgabgurus.common.decorators import db_sync_to_async
from gabgabgurus.common.mixins.serializer import AsyncSerializerMixin
from gabgabgurus.config.exceptions import Forbidden


class ChatConsumerMessageHandler(AsyncSerializerMixin):
    def __init__(self, consumer):
        self.consumer = consumer

    async def handle_message(self, content):
        raise NotImplementedError("Method must be implemented by subclass")

    @property
    def user(self):
        return self.consumer.user

    @property
    def user_id(self):
        return self.user.id

    async def get_recipient_ids(self, channel_id: int):
        channel_recipients = await self.get_channel_recipient_ids(channel_id)
        connected_users = get_chat_connected_users(channel_id)
        recipients = channel_recipients - connected_users
        return recipients

    @db_sync_to_async
    def get_channel_recipient_ids(self, channel_id: int):
        participants = get_channel_members(channel_id, self.user_id)
        return {participant.id for participant in participants}

    async def get_serializer_context(self):
        return {"request": getattr(self.consumer, "request", None)}


class CreateMessageHandler(ChatConsumerMessageHandler):
    serializer_class = MessageRequest
    output_serializer_class = MessageResponse

    async def handle_message(self, content):
        validated_data = await self.validate(content)
        if not validated_data:
            return None

        created_message = await self.create_message(validated_data)
        if not created_message:
            return None

        await self.create_message_statuses_for_recipients(created_message, MessageStatuses.DELIVERED)

        created_message_from_db = await self.get_message_from_db(created_message.id)
        serialized_created_message = await self.get_output_serialized_data(created_message_from_db)
        await self.consumer.reply_all("send_chat_message", serialized_created_message)

        await self.send_notifications_to_all_recipients(
            validated_data["channel_id"],
            serialized_created_message,
        )

    async def validate(self, input_data):
        if not self.user.is_authenticated:
            raise Forbidden("User is not authenticated")

        validated_data = await self.get_validated_data(input_data)
        validated_data["sender"] = self.user

        return validated_data

    @db_sync_to_async
    def create_message(self, data):
        if data:
            return create_message(**data)
        return None

    @db_sync_to_async
    def get_message_from_db(self, message_id):
        return get_messages(filters={"id": message_id}, statuses=True).first()

    @db_sync_to_async
    def create_message_statuses_for_recipients(self, message, status: MessageStatuses | None = None):
        return create_message_statuses_for_recipients(message=message, sender=self.user, status=status)

    async def send_notifications_to_all_recipients(self, channel_id: int, created_message_data):
        recipient_ids = await self.get_recipient_ids(channel_id)
        for recipient_id in recipient_ids:
            await self.consumer.reply_all(
                "send_notification",
                created_message_data,
                group_name=make_user_notify_consumer_group_name(recipient_id),
            )


class UserBlockingHandler(ChatConsumerMessageHandler):
    serializer_class = MessageRequest
    output_serializer_class = MessageResponse

    async def handle_message(self, content):
        await self.consumer.reply_all(
            "send_chat_message",
            content,
            message_type=ChatMessageTypes.USER_BLOCKING.value,
        )


class MarkAsRedMessageHandler(ChatConsumerMessageHandler):
    serializer_class = MarkMessagesAsReadRequest
    output_serializer_class = MessageResponse

    async def handle_message(self, content):
        validated_data = await self.validate(content)
        if not validated_data:
            return None

        await self.mark_messages_as_read(validated_data)

        await self.consumer.reply_all(
            "send_chat_message",
            validated_data,
            message_type=ChatMessageTypes.USER_READ_MESSAGES,
        )

    async def validate(self, input_data):
        if not self.user.is_authenticated:
            raise Forbidden("User is not authenticated")

        validated_data = await self.get_validated_data(input_data)

        return validated_data

    @db_sync_to_async
    def mark_messages_as_read(self, data):
        if data:
            return mark_messages_as_read(**data)
        return None
