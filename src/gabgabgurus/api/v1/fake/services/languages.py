from faker import Faker

from gabgabgurus.api.v1.fake.utils import make_objects_by_names, save_objects
from gabgabgurus.apps.languages.models import Language

fake = Faker()


# @timer
def make_languages_names(n: int) -> set[str]:
    try:
        set_of_names = {fake.unique.language_name() for _ in range(n)}
    except Exception:
        set_of_names = {fake.language_name() for _ in range(n)}
    return set_of_names


# @timer
def filter_only_not_existing_languages(language_names: set[str]) -> set[str]:
    existing_languages = Language.objects.filter(name__in=language_names)
    existing_languages_names = set(existing_languages.values_list("name", flat=True))
    return language_names - existing_languages_names


# @timer
def generate_languages(n: int) -> int:
    languages_names = make_languages_names(n)
    unique_languages_names = filter_only_not_existing_languages(languages_names)
    unique_languages = make_objects_by_names(Language, unique_languages_names)
    save_objects(Language, unique_languages)
    return len(unique_languages)
