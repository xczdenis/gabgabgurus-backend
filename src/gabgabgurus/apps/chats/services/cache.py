from django.core.cache import cache


def make_chat_connected_users_cache_key(chat_id: int) -> str:
    return f"CHAT_CONSUMER_chat_{chat_id}_connected_users"


def add_user_to_chat_connected_users(user_id: int, chat_id: int):
    cache_key = make_chat_connected_users_cache_key(chat_id)
    connected_users = get_chat_connected_users(chat_id)
    connected_users.add(user_id)
    cache.set(cache_key, connected_users)


def remove_user_from_chat_connected_users(user_id: int, chat_id: int):
    cache_key = make_chat_connected_users_cache_key(chat_id)
    connected_users = get_chat_connected_users(chat_id)
    connected_users.remove(user_id)
    cache.set(cache_key, connected_users)


def get_chat_connected_users(chat_id: int) -> set:
    cache_key = make_chat_connected_users_cache_key(chat_id)

    result = cache.get(cache_key)
    if result is None:
        return set()

    return cache.get(cache_key)
