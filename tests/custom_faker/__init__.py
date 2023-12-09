from faker import Faker

from tests.custom_faker.providers import UserProvider

faker = Faker()

faker.add_provider(UserProvider)
