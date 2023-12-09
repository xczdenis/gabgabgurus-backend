import pytest

from gabgabgurus.apps.languages.models import Language


@pytest.fixture(scope="function")
def language_english(db):
    return Language.objects.create(name="English")


@pytest.fixture(scope="function")
def language_spanish(db):
    return Language.objects.create(name="Spanish")


@pytest.fixture(scope="function")
def language_bosnian(db):
    return Language.objects.create(name="Bosnian")


@pytest.fixture(scope="function")
def language_italian(db):
    return Language.objects.create(name="Italian")
