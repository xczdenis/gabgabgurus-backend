import os

from gabgabgurus.config import BASE_DIR
from gabgabgurus.config.settings import app_config

SECRET_KEY = app_config.SECRET_KEY

ALLOWED_HOSTS = app_config.get_allowed_hosts()

DJANGO_APPS = [
    "daphne",
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

THIRD_PARTIES_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
    "corsheaders",
    "drf_spectacular",
    "dj_rest_auth",
    "django_cleanup.apps.CleanupConfig",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.google",
    "django_admin_inline_paginator",
    "rangefilter",
]

PROJECT_APPS = [
    "gabgabgurus.apps.chats.apps.ChatsConfig",
    "gabgabgurus.apps.languages.apps.LanguagesConfig",
    "gabgabgurus.apps.users.apps.UsersConfig",
    "gabgabgurus.apps.management_commands.apps.ManagementCommandsConfig",
    "gabgabgurus.apps.user_details.apps.UserDetailsConfig",
    "gabgabgurus.apps.hobbies.apps.HobbiesConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTIES_APPS + PROJECT_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "gabgabgurus.config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "gabgabgurus.config.wsgi.application"
ASGI_APPLICATION = "gabgabgurus.config.asgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "api/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles/")

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Security
# https://docs.djangoproject.com/en/dev/topics/security/
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True

# CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = "DENY"

# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy
REFERRER_POLICY = "same-origin"

CSRF_TRUSTED_ORIGINS = app_config.get_csrf_trusted_origin_hosts()

AUTH_USER_MODEL = "users.User"

# CORS settings
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = app_config.get_cors_allowed_origin_hosts()
