from django.db import models
from django.utils.translation import gettext_lazy as _


class Hobby(models.Model):
    name = models.CharField(_("name"), max_length=250, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Hobby")
        verbose_name_plural = _("Hobbies")
        ordering = ("name",)
