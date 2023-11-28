from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserDetailsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gabgabgurus.apps.user_details"
    verbose_name = _("User details")
