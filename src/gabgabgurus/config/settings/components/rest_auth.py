from django.conf import settings

ACCESS_TOKEN_NAME = "access"  # noqa: S105 Possible hardcoded password
REFRESH_TOKEN_NAME = "refresh"  # noqa: S105 Possible hardcoded password

REST_AUTH = {
    "TOKEN_MODEL": None,
    "USE_JWT": True,
    "JWT_AUTH_SECURE": settings.DEBUG,
    "JWT_AUTH_COOKIE": ACCESS_TOKEN_NAME,
    "JWT_AUTH_REFRESH_COOKIE": REFRESH_TOKEN_NAME,
}
