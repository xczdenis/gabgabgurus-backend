from django.core.management.base import BaseCommand

from gabgabgurus.apps.hobbies.initializers import hobby_initializer
from gabgabgurus.apps.languages.initializers import country_initializer, language_initializer

DATA_INITIALIZERS = (language_initializer, country_initializer, hobby_initializer)


class Command(BaseCommand):
    def handle(self, *args, **options):
        for initializer in DATA_INITIALIZERS:
            initializer.initialize()
