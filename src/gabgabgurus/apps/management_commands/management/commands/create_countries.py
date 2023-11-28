import json

from django.core.management.base import BaseCommand
from loguru import logger

from gabgabgurus.apps.languages.models import Country
from gabgabgurus.apps.management_commands.constants import INIT_DATA_PATH

SOURCE_FILE_NAME = "countries_languages.json"
COUNTRY_COLUMN = "Country/Region"


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.load_countries()

    def load_countries(self):
        logger.info("Start creating countries")
        countries_to_create, count_in_db, count_in_file = self.get_countries_to_create()
        created_count = self.create_countries(countries_to_create)
        logger.info(f"In db before created: {count_in_db}")
        logger.info(f"In file: {count_in_file}")
        logger.info(f"New objects: {len(countries_to_create)}")
        logger.info(f"Created objects: {created_count}")
        logger.info("Countries created successfully")

    def get_countries_to_create(self) -> tuple[set, int, int]:
        from_db = self.get_countries_from_db()
        from_file = self.get_countries_from_file()
        return from_file - from_db, len(from_db), len(from_file)

    def get_countries_from_db(self) -> set:
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
        return INIT_DATA_PATH / SOURCE_FILE_NAME

    def create_countries(self, countries: set):
        countries_to_create = (Country(name=country_name) for country_name in countries)
        objs = Country.objects.bulk_create(countries_to_create)
        return len(objs)
