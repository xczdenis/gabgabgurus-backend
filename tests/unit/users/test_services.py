import pytest

from gabgabgurus.apps.users.services import make_user_notify_consumer_group_name

pytestmark = pytest.mark.unit


@pytest.mark.parametrize("user_id", (None, 0, 999999999999999, -1))
def test_make_user_notify_consumer_group_name(user_id):
    expected = f"NOTIFICATIONS_{user_id}"

    actual = make_user_notify_consumer_group_name(user_id)

    assert expected == actual
