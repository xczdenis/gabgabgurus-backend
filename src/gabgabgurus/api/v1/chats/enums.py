from enum import Enum


class ChatMessageTypes(str, Enum):
    MESSAGE = "message"
    MARK_AS_READ_MESSAGE = "mark_as_read"
    USER_JOINED = "user_joined"
    USER_BLOCKING = "user_blocking"
    USER_READ_MESSAGES = "user_read_messages"
