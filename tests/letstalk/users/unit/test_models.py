import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker

User = get_user_model()

pytestmark = pytest.mark.unit


class TestUser:
    @pytest.mark.django_db
    def test_string_representation(self):
        user = baker.prepare(User, _fill_optional=True)

        assert str(user) == user.email
