import pytest
from django.db import IntegrityError

from gabgabgurus.apps.languages.models import CountryLanguage

# @pytest.fixture(scope="function")
# def country_language(country_italy, language_italian):
#     return CountryLanguage.objects.create(country=country_cuba, language=language_english, is_official=True)


def test_country_language_creation(country_italy, language_italian):
    new_country_language = CountryLanguage.objects.create(country=country_italy, language=language_italian)

    assert new_country_language.country == country_italy
    assert new_country_language.language == language_italian


def test_string_representation(country_italy, language_italian):
    new_country_language = CountryLanguage.objects.create(country=country_italy, language=language_italian)
    expected = str(new_country_language.id)

    actual = str(new_country_language)

    assert actual == expected


def test_unique_constraint_violation(country_italy, language_italian):
    CountryLanguage.objects.create(country=country_italy, language=language_italian)

    with pytest.raises(IntegrityError):
        CountryLanguage.objects.create(country=country_italy, language=language_italian)


def test_unique_constraint_success(country_italy, country_cuba, language_italian):
    item1 = CountryLanguage.objects.create(country=country_italy, language=language_italian)
    item2 = CountryLanguage.objects.create(country=country_cuba, language=language_italian)

    assert item1 is not None
    assert item2 is not None
