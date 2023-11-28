from channels.generic.websocket import AsyncJsonWebsocketConsumer

from gabgabgurus.api.v1.chats.enums import ChatMessageTypes
from gabgabgurus.api.v1.chats.factories import ChatMessageHandlerFactory
from gabgabgurus.api.ws_error_handlers import async_exception_handling
from gabgabgurus.apps.chats.services.cache import (
    add_user_to_chat_connected_users,
    remove_user_from_chat_connected_users,
)
from gabgabgurus.apps.chats.services.ws import make_chat_consumer_group_name
from gabgabgurus.common.mixins.websocket import GroupWebsocketConsumerMixin


@async_exception_handling()
class ChatConsumer(GroupWebsocketConsumerMixin, AsyncJsonWebsocketConsumer):
    url_param_chat_id = "chat_id"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connected_users = set()

    @property
    def chat_id(self):
        return self.url_kwargs.get(ChatConsumer.url_param_chat_id)

    @property
    def user_id(self):
        return self.user.id

    async def get_group_name(self):
        return make_chat_consumer_group_name(self.chat_id)

    async def join_to_group(self, group_name=None):
        await super().join_to_group(group_name)
        add_user_to_chat_connected_users(self.user_id, self.chat_id)

    async def leave_group(self, group_name=None):
        await super().join_to_group(group_name)
        remove_user_from_chat_connected_users(self.user_id, self.chat_id)

    async def connect(self):
        await self.join_to_group()
        await super().connect()
        message_data = {"id": self.user.id}
        await self.reply_all(
            "send_chat_message",
            message_data,
            ChatMessageTypes.USER_JOINED.value,
        )

    async def disconnect(self, close_code):
        await self.leave_group()

    async def receive_json(self, content, **kwargs):
        handler = await self.get_message_handler(content)
        if handler:
            await handler.handle_message(content)

    async def get_message_handler(self, content):
        client_message_type = await self.get_client_message_type(content)
        return ChatMessageHandlerFactory.get_handler(self, client_message_type)

    async def send_chat_message(self, event):
        message = event["payload"]
        await self.send_json(message)
