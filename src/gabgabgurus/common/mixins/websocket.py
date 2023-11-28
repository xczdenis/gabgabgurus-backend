from typing import Any

from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer
from django.core.handlers.asgi import ASGIRequest
from loguru import logger
from orjson import orjson

from gabgabgurus.common.mixins.serializer import AsyncSerializerMixin
from gabgabgurus.common.utils.exceptions import (
    exc_is_available_to_notify_ws_client,
    extract_exception_details,
    make_log_message,
)
from gabgabgurus.config.constants import WS_DEFAULT_MESSAGE_TYPE, WS_ERROR_MESSAGE_TYPE


class ASGIRequestConsumerMixin(AsyncWebsocketConsumer):
    async def connect(self):
        await self.update_scope(method="WS")
        await self.init_asgi_request()
        await super().connect()

    async def update_scope(self, **kwargs):
        self.scope.update(kwargs)

    async def init_asgi_request(self):
        request = await self.create_asgi_request()
        setattr(self, "request", request)

    async def create_asgi_request(self):
        return ASGIRequest(self.scope, None)


class ScopeMixin:
    scope = {}

    @property
    def user(self):
        return self.scope.get("user")

    @property
    def url_route(self):
        return self.scope.get("url_route") or {}

    @property
    def url_args(self):
        return self.url_route.get("args") or {}

    @property
    def url_kwargs(self):
        return self.url_route.get("kwargs") or {}


class BaseWebsocketConsumerMixin(ASGIRequestConsumerMixin, ScopeMixin, AsyncJsonWebsocketConsumer):
    message_type_key = "type"
    message_content_key = "content"
    message_type_key_from_client = "__ws_message_type"

    async def on_error(self, exc, *args, **kwargs):
        log_message = make_log_message(exc, **kwargs)
        logger.error(log_message)
        await self.notify_client_on_exception(exc)

    async def notify_client_on_exception(self, exc):
        if await exc_is_available_to_notify_ws_client(exc):
            details = extract_exception_details(exc)
        else:
            details = "Internal server error"
        message = await self.make_error_message(details)
        await self.send_json(message)

    async def make_error_message(self, content):
        return await self.make_message(content, WS_ERROR_MESSAGE_TYPE)

    async def make_message(self, content, message_type) -> dict:
        return {self.message_type_key: message_type, self.message_content_key: content}

    async def get_client_message_type(self, content):
        return content.get(self.message_type_key_from_client, None)

    @classmethod
    async def decode_json(cls, text_data):
        return orjson.loads(text_data)

    @classmethod
    async def encode_json(cls, content):
        return orjson.dumps(content).decode()


class DataWebsocketConsumerMixin(AsyncSerializerMixin, BaseWebsocketConsumerMixin):
    pass


class GroupWebsocketConsumerMixin(DataWebsocketConsumerMixin):
    async def join_to_group(self, group_name=None):
        group = group_name or await self.get_group_name()
        await self.channel_layer.group_add(group, self.channel_name)

    async def leave_group(self, group_name=None):
        group = group_name or await self.get_group_name()
        await self.channel_layer.group_discard(group, self.channel_name)

    async def reply_all(
        self,
        method_name: str,
        data: Any,
        message_type: str = WS_DEFAULT_MESSAGE_TYPE,
        group_name=None,
    ):
        if data is not None:
            group = group_name or await self.get_group_name()
            message = await self.make_message(data, message_type)
            action = {"type": method_name, "payload": message}
            await self.channel_layer.group_send(group, action)

    async def get_group_name(self):
        raise NotImplementedError("Method must be implemented by subclass")
