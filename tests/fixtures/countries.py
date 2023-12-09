import pytest

from gabgabgurus.apps.languages.models import Country


@pytest.fixture(scope="function")
def country_botswana(db):
    return Country.objects.create(name="Botswana")


@pytest.fixture(scope="function")
def country_chile(db):
    return Country.objects.create(name="Chile")


@pytest.fixture(scope="function")
def country_cuba(db):
    return Country.objects.create(name="Cuba")


@pytest.fixture(scope="function")
def country_italy(db):
    return Country.objects.create(name="Italy")
