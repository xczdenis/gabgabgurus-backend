import json

from django.core.management.base import BaseCommand
from loguru import logger

from gabgabgurus.apps.languages.models import Language
from gabgabgurus.apps.management_commands.constants import INIT_DATA_PATH

SOURCE_FILE_NAME = "countries_languages.json"
LANGUAGE_COLUMN = "Official language"


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.load_languages()

    def load_languages(self):
        logger.info("Start creating languages")
        languages_to_create, count_in_db, count_in_file = self.get_languages_to_create()
        created_count = self.create_languages(languages_to_create)
        logger.info(f"In db before created: {count_in_db}")
        logger.info(f"In file: {count_in_file}")
        logger.info(f"New objects: {len(languages_to_create)}")
        logger.info(f"Created objects: {created_count}")
        logger.info("Languages created successfully")

    def get_languages_to_create(self) -> tuple[set, int, int]:
        from_db = self.get_languages_from_db()
        from_file = self.get_languages_from_file()
        return from_file - from_db, len(from_db), len(from_file)

    def get_languages_from_db(self) -> set:
        return set(Language.objects.all().values_list("name", flat=True))

    def get_languages_from_file(self) -> set:
        languages = set()

        file_path = self.get_file_path()
        with open(file_path, "r") as f:
            data = json.load(f)

        for record in data:
            language_list = record.get(LANGUAGE_COLUMN)
            if language_list:
                languages.update(language_list)

        return languages

    def get_file_path(self):
        return INIT_DATA_PATH / SOURCE_FILE_NAME

    def create_languages(self, languages: set):
        languages_to_create = (Language(name=language_name) for language_name in languages)
        objs = Language.objects.bulk_create(languages_to_create)
        return len(objs)
