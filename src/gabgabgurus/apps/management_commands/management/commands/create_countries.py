from django.core.management.base import BaseCommand

from gabgabgurus.apps.languages.initializers import country_initializer


class Command(BaseCommand):
    def handle(self, *args, **options):
        country_initializer.initialize()
