import pytest
from django.contrib.auth import get_user_model

from gabgabgurus.apps.users.services import create_superuser_if_not_exists
from gabgabgurus.config.exceptions import EntityAlreadyExists

User = get_user_model()


@pytest.mark.django_db
def test_with_new_superuser():
    email = "newsuperuser@example.com"
    password = "testpassword123"

    superuser = create_superuser_if_not_exists(email=email, password=password)

    assert superuser is not None
    assert superuser.email == email
    assert superuser.is_superuser


@pytest.mark.django_db
def test_with_existing_superuser():
    email = "existingsuperuser@example.com"
    password = "testpassword123"

    User.objects.create_superuser(email=email, password=password)

    with pytest.raises(EntityAlreadyExists):
        create_superuser_if_not_exists(email=email, password=password)
