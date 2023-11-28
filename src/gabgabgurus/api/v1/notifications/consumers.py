from channels.generic.websocket import AsyncJsonWebsocketConsumer

from gabgabgurus.api.v1.chats.serializers.messages import MessageRequest, MessageResponse
from gabgabgurus.api.ws_error_handlers import async_exception_handling
from gabgabgurus.apps.users.services import make_user_notify_consumer_group_name
from gabgabgurus.common.mixins.websocket import GroupWebsocketConsumerMixin


@async_exception_handling()
class UserNotifyConsumer(GroupWebsocketConsumerMixin, AsyncJsonWebsocketConsumer):
    url_param = "user_id"
    serializer_class = MessageRequest
    output_serializer_class = MessageResponse

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def get_group_name(self):
        return make_user_notify_consumer_group_name(self.user.id)

    async def connect(self):
        await self.join_to_group()
        await super().connect()

    async def disconnect(self, close_code):
        await self.leave_group()

    async def send_notification(self, event):
        message = event["payload"]
        await self.send_json(message)
