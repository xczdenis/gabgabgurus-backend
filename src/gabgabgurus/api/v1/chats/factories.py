from dataclasses import dataclass

from gabgabgurus.api.v1.chats.enums import ChatMessageTypes
from gabgabgurus.api.v1.chats.handlers import (
    CreateMessageHandler,
    MarkAsRedMessageHandler,
    UserBlockingHandler,
)


@dataclass(slots=True, frozen=True)
class ChatMessageHandlerFactory:
    handlers = {
        ChatMessageTypes.MESSAGE: CreateMessageHandler,
        ChatMessageTypes.USER_BLOCKING: UserBlockingHandler,
        ChatMessageTypes.MARK_AS_READ_MESSAGE: MarkAsRedMessageHandler,
    }

    @classmethod
    def get_handler(cls, consumer, message_type):
        handler_class = cls.handlers.get(message_type)
        if handler_class:
            return handler_class(consumer=consumer)

        return None
