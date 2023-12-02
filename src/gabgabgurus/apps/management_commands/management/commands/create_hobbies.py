from django.core.management.base import BaseCommand

from gabgabgurus.apps.hobbies.initializers import hobby_initializer


class Command(BaseCommand):
    def handle(self, *args, **options):
        hobby_initializer.initialize()
