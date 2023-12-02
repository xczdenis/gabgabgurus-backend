import json
from dataclasses import dataclass

from loguru import logger

from gabgabgurus.apps.languages.models import Country, Language
from gabgabgurus.apps.management_commands.constants import INIT_DATA_PATH
from gabgabgurus.common.interfaces import DataInitializer

LANGUAGE_COLUMN = "Official language"
COUNTRY_COLUMN = "Country/Region"


@dataclass
class LanguageInitializer(DataInitializer):
    source_file_name: str

    def initialize(self):
        self.load_languages()

    def load_languages(self):
        logger.info("Start creating languages")
        languages_to_create, count_in_db, count_in_file = self.get_languages_to_create()
        created_count = self.create_languages(languages_to_create)
        logger.info(f"In db before created: {count_in_db}")
        logger.info(f"In file: {count_in_file}")
        logger.info(f"New objects: {len(languages_to_create)}")
        logger.info(f"Created objects: {created_count}")
        logger.success("Languages created successfully")

    def get_languages_to_create(self) -> tuple[set, int, int]:
        from_db = self.get_languages_from_db()
        from_file = self.get_languages_from_file()
        return from_file - from_db, len(from_db), len(from_file)

    @classmethod
    def get_languages_from_db(cls) -> set:
        return set(Language.objects.all().values_list("name", flat=True))

    def get_languages_from_file(self) -> set:
        languages = set()

        with open(self.get_file_path(), "r") as f:
            data = json.load(f)

        for record in data:
            language_list = record.get(LANGUAGE_COLUMN)
            if language_list:
                languages.update(language_list)

        return languages

    def get_file_path(self):
        return INIT_DATA_PATH / self.source_file_name

    @classmethod
    def create_languages(cls, languages: set):
        languages_to_create = (Language(name=language_name) for language_name in languages)
        objs = Language.objects.bulk_create(languages_to_create)
        return len(objs)


@dataclass
class CountryInitializer(DataInitializer):
    source_file_name: str

    def initialize(self):
        self.load_countries()

    def load_countries(self):
        logger.info("Start creating countries")
        countries_to_create, count_in_db, count_in_file = self.get_countries_to_create()
        created_count = self.create_countries(countries_to_create)
        logger.info(f"In db before created: {count_in_db}")
        logger.info(f"In file: {count_in_file}")
        logger.info(f"New objects: {len(countries_to_create)}")
        logger.info(f"Created objects: {created_count}")
        logger.success("Countries created successfully")

    def get_countries_to_create(self) -> tuple[set, int, int]:
        from_db = self.get_countries_from_db()
        from_file = self.get_countries_from_file()
        return from_file - from_db, len(from_db), len(from_file)

    @classmethod
    def get_countries_from_db(cls) -> set:
        return set(Country.objects.all().values_list("name", flat=True))

    def get_countries_from_file(self) -> set:
        countries = set()

        file_path = self.get_file_path()
        with open(file_path, "r") as f:
            data = json.load(f)

        for record in data:
            country = record.get(COUNTRY_COLUMN)
            if country:
                countries.add(country)

        return countries

    def get_file_path(self):
        return INIT_DATA_PATH / self.source_file_name

    @classmethod
    def create_countries(cls, countries: set):
        countries_to_create = (Country(name=country_name) for country_name in countries)
        objs = Country.objects.bulk_create(countries_to_create)
        return len(objs)


language_initializer = LanguageInitializer(source_file_name="countries_languages.json")
country_initializer = CountryInitializer(source_file_name="countries_languages.json")
