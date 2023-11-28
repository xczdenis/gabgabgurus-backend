from functools import wraps
from typing import Callable

from channels.db import database_sync_to_async


def default(**default_kwargs) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for key, value in default_kwargs.items():
                kwargs.setdefault(key, value)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def db_sync_to_async(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return await database_sync_to_async(func)(*args, **kwargs)

    return wrapper
