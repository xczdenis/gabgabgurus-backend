from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ManagementCommandsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gabgabgurus.apps.management_commands"
    verbose_name = _("Management commands")
