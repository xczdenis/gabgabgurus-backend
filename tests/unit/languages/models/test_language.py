import pytest
from model_bakery import baker

from gabgabgurus.apps.languages.models import Language


@pytest.mark.django_db
def test_string_representation():
    language = baker.prepare(Language, _fill_optional=True)

    assert str(language) == language.name


@pytest.mark.django_db
def test_ordering():
    names_in_wrong_order = ["z", "d", "a"]
    for name in names_in_wrong_order:
        Language.objects.create(name=name)
    names_in_wrong_order.sort()
    expected = str(names_in_wrong_order)

    names_from_db = list(Language.objects.all().values_list("name", flat=True))
    actual = str(names_from_db)

    assert actual == expected
