from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils import timezone

from gabgabgurus.config.constants import CACHE_PREFIX_USER_LAST_ACTIVITY, USER_LAST_ACTIVITY_CACHE_TTL_SECONDS
from gabgabgurus.config.exceptions import EntityAlreadyExists

User = get_user_model()


def create_user_if_not_exists(email: str, password: str, **extra_fields) -> User:
    if not user_exists(email):
        return create_user(email, password, **extra_fields)
    raise EntityAlreadyExists("User with email {email} already exists".format(email=email))


def create_superuser_if_not_exists(email: str, password: str, **extra_fields) -> User:
    if not user_exists(email):
        return create_superuser(email, password, **extra_fields)
    raise EntityAlreadyExists("User with email {email} already exists".format(email=email))


def user_exists(email: str) -> bool:
    return User.objects.filter(email__iexact=email).exists()


def create_user(email: str, password: str, **extra_fields) -> User:
    return User.objects.create_user(email, password, **extra_fields)


def create_superuser(email: str, password: str, **extra_fields) -> User:
    return User.objects.create_superuser(email, password, **extra_fields)


def update_user_last_login(user_id: int, last_login=None):
    _last_login = last_login if last_login is not None else timezone.now()
    User.objects.filter(id=user_id).update(last_login=_last_login)


def make_cache_key_user_last_activity(user_id):
    return f"{CACHE_PREFIX_USER_LAST_ACTIVITY}_{user_id}"


def make_user_notify_consumer_group_name(user_id: int):
    return f"NOTIFICATIONS_{user_id}"


def set_user_last_activity_in_cache(user_id: int):
    cache_key = make_cache_key_user_last_activity(user_id)
    cache.set(cache_key, timezone.now(), timeout=USER_LAST_ACTIVITY_CACHE_TTL_SECONDS)
