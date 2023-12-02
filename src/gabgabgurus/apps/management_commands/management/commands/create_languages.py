from django.core.management.base import BaseCommand

from gabgabgurus.apps.languages.initializers import language_initializer


class Command(BaseCommand):
    def handle(self, *args, **options):
        language_initializer.initialize()
