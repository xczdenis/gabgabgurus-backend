from gabgabgurus.config import redis_config

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{redis_config.REDIS_HOST}:{redis_config.REDIS_PORT}",
    }
}
