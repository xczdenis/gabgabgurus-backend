import pytest
from django.contrib.auth import get_user_model

from gabgabgurus.apps.user_details.models import UserLanguage
from gabgabgurus.apps.user_details.services import update_user_language

User = get_user_model()


@pytest.fixture(scope="function")
def test_user_language(existing_user_and_his_password, language_english):
    user, _ = existing_user_and_his_password
    return UserLanguage.objects.create(user=user, language=language_english)


def test(test_user_language, language_spanish):
    new_data = {"language": language_spanish}
    expected_language = language_spanish.name

    updated_user_language = update_user_language(test_user_language, new_data)
    actual_language = updated_user_language.language.name

    assert expected_language == actual_language
