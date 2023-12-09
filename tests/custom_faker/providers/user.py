from django.contrib.auth import get_user_model
from faker import Faker
from faker.providers import BaseProvider

from tests.utils.decorators import test_prefix
from tests.utils.models import make_resource_id

User = get_user_model()

local_faker = Faker()


class UserProvider(BaseProvider):
    def app_users(self, items_number: int) -> list[User]:
        return [self.app_user() for _ in range(items_number)]

    def app_user(self, email: str = "", pwd: str = "") -> User:
        user = User()
        user.id = make_resource_id()
        user.email = email or self.app_user_email()
        user.set_password(pwd or local_faker.password())
        return user

    @test_prefix
    def app_user_email(self) -> str:
        return local_faker.user_email()

    @test_prefix
    def unique_user_email(self) -> str:
        email_mask = "unique-{n}@gmail.com"
        n = 0
        email = email_mask.format(n=n)
        while User.objects.filter(email=email).first() is not None:
            n += 1
            email = email_mask.format(n=n)
        return email
