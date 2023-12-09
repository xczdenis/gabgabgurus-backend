import pytest
from django.contrib.auth import get_user_model

from gabgabgurus.apps.users.services import create_user_if_not_exists
from gabgabgurus.config.exceptions import EntityAlreadyExists

User = get_user_model()


@pytest.mark.django_db
def test_with_new_user():
    email = "newuser@example.com"
    password = "testpassword123"

    user = create_user_if_not_exists(email=email, password=password)

    assert user is not None
    assert user.email == email


@pytest.mark.django_db
def test_with_existing_user():
    email = "existinguser@example.com"
    password = "testpassword123"

    User.objects.create_user(email=email, password=password)

    with pytest.raises(EntityAlreadyExists):
        create_user_if_not_exists(email=email, password=password)
