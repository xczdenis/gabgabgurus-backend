from gabgabgurus.config.constants import EXCEPTIONS_FOR_WS_CLIENT_REPLY


def extract_exception_details(exception: Exception) -> dict:
    data = {"detail": ""}
    if hasattr(exception, "detail"):
        if isinstance(exception.detail, dict):
            data = exception.detail
        else:
            data["detail"] = exception.detail
    elif hasattr(exception, "description"):
        data["detail"] = exception.description
    elif hasattr(exception, "message"):
        data["detail"] = exception.message
    else:
        data["detail"] = str(exception)
    return data


def make_log_message(exc: Exception, **kwargs) -> str:
    func = kwargs.get("func")
    error_source = f"{func.__qualname__}. " if func is not None else ""
    return f"{error_source}{type(exc).__name__}: {exc}"


async def exc_is_available_to_notify_ws_client(exc):
    return type(exc) in EXCEPTIONS_FOR_WS_CLIENT_REPLY
