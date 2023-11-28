from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HobbiesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gabgabgurus.apps.hobbies"
    verbose_name = _("Hobbies")
