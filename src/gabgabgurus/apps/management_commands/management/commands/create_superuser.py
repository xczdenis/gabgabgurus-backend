from django.core.management.base import BaseCommand
from loguru import logger

from gabgabgurus.apps.users.services import create_superuser, user_exists
from gabgabgurus.config import app_config


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = app_config.SUPERUSER_EMAIL
        if not user_exists(email):
            create_superuser(email, app_config.SUPERUSER_PASSWORD, first_name="admin", last_name="admin")
            logger.success("Superuser successfully created")
        else:
            logger.info("Superuser already exists")
