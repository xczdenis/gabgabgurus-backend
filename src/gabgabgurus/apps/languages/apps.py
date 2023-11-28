from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LanguagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gabgabgurus.apps.languages"
    verbose_name = _("Languages")
