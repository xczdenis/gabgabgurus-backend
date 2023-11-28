from functools import wraps
from inspect import iscoroutinefunction

from channels.exceptions import AcceptConnection, DenyConnection, StopConsumer


def async_exception_handling(raise_exception=False):
    def decorator(consumer_class):
        for method_name, method in list(consumer_class.__dict__.items()):
            if iscoroutinefunction(method) and method_name != "on_error":
                setattr(consumer_class, method_name, propagate_async_exceptions(raise_exception)(method))
        return consumer_class

    return decorator


def propagate_async_exceptions(raise_exception=False):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except (AcceptConnection, DenyConnection, StopConsumer):
                raise
            except Exception as e:
                if not getattr(e, "__exc_already_caught__", False):
                    setattr(e, "__exc_already_caught__", True)
                    await async_websocket_exception_handler(e, *args, func=func, **kwargs)

                if raise_exception:
                    raise

        return wrapper

    return decorator


async def async_websocket_exception_handler(exc, *args, **kwargs):
    error_handler = getattr(args[0], "on_error", None) if args else None
    if error_handler is not None:
        await error_handler(exc, *args, **kwargs)
