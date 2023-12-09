import pytest
from django.contrib.auth import get_user_model

from gabgabgurus.apps.users.services import user_exists

User = get_user_model()


@pytest.mark.django_db
def test_with_existing_user():
    user = User.objects.create_user(email="test@example.com", password="test")
    expected = True

    actual = user_exists(user.email)

    assert actual == expected


@pytest.mark.django_db
def test_with_non_existing_user():
    nonexistent_email = "nonexistent@example.com"
    expected = False

    actual = user_exists(nonexistent_email)

    assert actual == expected
