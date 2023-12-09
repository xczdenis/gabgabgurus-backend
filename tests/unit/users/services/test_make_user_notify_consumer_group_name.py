import pytest

from gabgabgurus.apps.users.services import make_user_notify_consumer_group_name


@pytest.mark.parametrize("user_id", (None, 0, 1, 999999999999999, -1))
def test(user_id):
    expected = f"NOTIFICATIONS_{user_id}"

    actual = make_user_notify_consumer_group_name(user_id)

    assert actual == expected
