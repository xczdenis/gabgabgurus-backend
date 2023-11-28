from django.contrib.auth import get_user_model

from gabgabgurus.apps.languages.models import Language
from gabgabgurus.apps.user_details.models import UserLanguage
from gabgabgurus.common.utils.models import get_model_instance, save

User = get_user_model()


def create_update_user_language(user: User, data: dict) -> UserLanguage:
    language_name = data["language"]
    if isinstance(language_name, Language):
        language_name = language_name.name
    user_language = user.user_languages.filter(language__name=language_name).first()
    if user_language:
        return update_user_language(user_language, data)
    return create_user_language(user, data)


def create_user_language(user: User, data: dict) -> UserLanguage:
    data["language"] = get_model_instance(data["language"], Language, "name")
    new_user_language = UserLanguage(**data)
    new_user_language.user = user
    return save(new_user_language)


def update_user_language(user_language: UserLanguage, data: dict) -> UserLanguage:
    for field, value in data.items():
        setattr(user_language, field, value)
    save(user_language)
    return user_language
