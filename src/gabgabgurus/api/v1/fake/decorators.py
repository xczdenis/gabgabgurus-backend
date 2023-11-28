import time
from functools import wraps

from loguru import logger


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        logger.debug(f"Elapsed time for func '{func.__name__}' = {end - start}")
        return r

    return wrapper
