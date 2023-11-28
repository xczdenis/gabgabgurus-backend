import random
from functools import lru_cache

from django.contrib.auth import get_user_model
from faker import Faker

from gabgabgurus.api.v1.fake.utils import save_objects
from gabgabgurus.apps.languages.models import Country

User = get_user_model()

fake = Faker()


# @timer
def make_emails(n: int) -> set[str]:
    try:
        set_of_names = {fake.unique.email() for _ in range(n)}
    except Exception:
        set_of_names = {fake.email() for _ in range(n)}
    return set_of_names


# @timer
def filter_only_not_existing_emails(set_of_emails: set[str]) -> set[str]:
    existing_users = User.objects.filter(email__in=set_of_emails)
    existing_emails = set(existing_users.values_list("email", flat=True))
    return set_of_emails - existing_emails


# @timer
def make_user_by_email(email: str) -> User:
    first_name = fake.first_name()
    last_name = fake.last_name()
    country = get_country()
    return User(  # noqa: S106
        email=email,
        password="1",
        first_name=first_name,
        last_name=last_name,
        country=country,
    )


def get_country() -> Country:
    pk_min, pk_max = get_country_range()
    number = random.randint(pk_min, pk_max)  # noqa: S311
    return Country.objects.get(pk=number)


@lru_cache
def get_country_range() -> tuple[int, int]:
    objects = Country.objects.order_by("id")
    pk_min = objects.first().pk
    pk_max = objects.last().pk
    return pk_min, pk_max


def make_users_by_emails(emails) -> list[User]:
    return [make_user_by_email(email) for email in emails]


# @timer
def generate_users(n: int) -> int:
    emails = make_emails(n)
    unique_emails = filter_only_not_existing_emails(emails)
    unique_users = make_users_by_emails(unique_emails)
    save_objects(User, unique_users)
    return len(unique_users)
