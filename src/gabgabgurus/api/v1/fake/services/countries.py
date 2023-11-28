from faker import Faker

from gabgabgurus.api.v1.fake.utils import make_objects_by_names, save_objects
from gabgabgurus.apps.languages.models import Country

fake = Faker()


# @timer
def make_country_names(n: int) -> set[str]:
    try:
        set_of_names = {fake.unique.country() for _ in range(n)}
    except Exception:
        set_of_names = {fake.unique.country() for _ in range(n)}
    return set_of_names


# @timer
def filter_only_not_existing_countries(country_names: set[str]) -> set[str]:
    existing_countries = Country.objects.filter(name__in=country_names)
    existing_country_names = set(existing_countries.values_list("name", flat=True))
    return country_names - existing_country_names


# @timer
def generate_countries(n: int) -> int:
    country_names = make_country_names(n)
    unique_country_names = filter_only_not_existing_countries(country_names)
    unique_countries = make_objects_by_names(Country, unique_country_names)
    save_objects(Country, unique_countries)
    return len(unique_countries)
