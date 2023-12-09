import pytest

from gabgabgurus.apps.users.services import make_cache_key_user_last_activity
from gabgabgurus.config.constants import CACHE_PREFIX_USER_LAST_ACTIVITY


@pytest.mark.parametrize("user_id", (None, 0, 1, 999999999999999, -1))
def test(user_id):
    expected = f"{CACHE_PREFIX_USER_LAST_ACTIVITY}_{user_id}"

    actual = make_cache_key_user_last_activity(user_id)

    assert actual == expected
