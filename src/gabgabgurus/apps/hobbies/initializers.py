import json
from dataclasses import dataclass

from loguru import logger

from gabgabgurus.apps.hobbies.models import Hobby
from gabgabgurus.apps.management_commands.constants import INIT_DATA_PATH
from gabgabgurus.common.interfaces import DataInitializer


@dataclass
class HobbyInitializer(DataInitializer):
    source_file_name: str

    def initialize(self):
        self.load_hobbies()

    def load_hobbies(self):
        logger.info("Start creating hobbies")
        hobbies_to_create, count_in_db, count_in_file = self.get_hobbies_to_create()
        created_count = self.create_hobbies(hobbies_to_create)
        logger.info(f"In db before created: {count_in_db}")
        logger.info(f"In file: {count_in_file}")
        logger.info(f"New objects: {len(hobbies_to_create)}")
        logger.info(f"Created objects: {created_count}")
        logger.success("Hobbies created successfully")

    def get_hobbies_to_create(self) -> tuple[set, int, int]:
        from_db = self.get_hobbies_from_db()
        from_file = self.get_hobbies_from_file()
        return from_file - from_db, len(from_db), len(from_file)

    @classmethod
    def get_hobbies_from_db(cls) -> set:
        return set(Hobby.objects.all().values_list("name", flat=True))

    def get_hobbies_from_file(self) -> set:
        with open(self.get_file_path(), "r") as f:
            hobby_list = json.load(f)
        return set(hobby_list)

    def get_file_path(self):
        return INIT_DATA_PATH / self.source_file_name

    @classmethod
    def create_hobbies(cls, hobbies: set):
        hobbies_to_create = (Hobby(name=hobby_name) for hobby_name in hobbies)
        objs = Hobby.objects.bulk_create(hobbies_to_create)
        return len(objs)


hobby_initializer = HobbyInitializer(source_file_name="hobbies.json")
