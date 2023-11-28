from gabgabgurus.config import pg_config

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": pg_config.POSTGRES_DB,
        "USER": pg_config.POSTGRES_USER,
        "PASSWORD": pg_config.POSTGRES_PASSWORD,
        "HOST": pg_config.POSTGRES_HOST,
        "PORT": pg_config.POSTGRES_PORT,
    },
}

CONN_MAX_AGE = 10
