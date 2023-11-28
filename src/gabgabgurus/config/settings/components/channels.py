from gabgabgurus.config import redis_config

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(redis_config.REDIS_HOST, redis_config.REDIS_PORT)],
        },
    }
}
