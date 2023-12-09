# import faker
import pytest
from django.contrib.auth import get_user_model

from tests.custom_faker import faker

User = get_user_model()


@pytest.fixture(scope="function")
def existing_user_and_his_password(db) -> tuple[User, str]:
    unique_user_login = faker.unique_user_email()
    password = "Password123!"

    user = faker.app_user(unique_user_login, password)
    user.save()

    return user, password
