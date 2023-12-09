import pytest
from model_bakery import baker

from gabgabgurus.apps.hobbies.models import Hobby


@pytest.mark.django_db
def test_string_representation():
    hobby = baker.prepare(Hobby, _fill_optional=True)

    assert str(hobby) == hobby.name


@pytest.mark.django_db
def test_ordering():
    names_in_wrong_order = ["z", "d", "a"]
    for name in names_in_wrong_order:
        Hobby.objects.create(name=name)
    names_in_wrong_order.sort()
    expected = str(names_in_wrong_order)

    names_from_db = list(Hobby.objects.all().values_list("name", flat=True))
    actual = str(names_from_db)

    assert actual == expected
