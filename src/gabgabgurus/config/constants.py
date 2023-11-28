from rest_framework.exceptions import ValidationError

from gabgabgurus.config.exceptions import Forbidden, NonSensitiveException, NotRequiredContent

EXCEPTIONS_FOR_WS_CLIENT_REPLY = (
    ValidationError,
    NonSensitiveException,
    Forbidden,
    NotRequiredContent,
)

CACHE_PREFIX_USER_LAST_ACTIVITY = "__user_last_activity"
USER_LAST_ACTIVITY_CACHE_TTL_SECONDS = 7 * 24 * 60 * 60  # 1 week

WS_DEFAULT_MESSAGE_TYPE = "message"
WS_ERROR_MESSAGE_TYPE = "error"
