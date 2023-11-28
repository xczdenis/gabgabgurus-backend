from django.db import models
from django.utils.translation import gettext_lazy as _


class Language(models.Model):
    name = models.CharField(_("name"), max_length=250, unique=True, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")
        ordering = ("name",)


class Country(models.Model):
    name = models.CharField(_("name"), max_length=250, unique=True, blank=False)
    languages = models.ManyToManyField(Language, through="CountryLanguage", related_name="countries")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        ordering = ("name",)


class CountryLanguage(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="country_languages")
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="country_languages")
    is_official = models.BooleanField(_("is_official"), default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _("Country language")
        verbose_name_plural = _("Country languages")
        constraints = (
            models.UniqueConstraint(fields=("country", "language"), name="unique_country_language"),
        )
