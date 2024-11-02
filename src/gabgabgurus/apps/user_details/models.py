from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from gabgabgurus.apps.languages.enums import LanguageLevels
from gabgabgurus.apps.languages.models import Language

User = get_user_model()


class UserLanguage(models.Model):
    related_name = "user_languages"
    user_native_speakers_filter = {
        f"{related_name}__is_speaking": True,
        f"{related_name}__language_level": LanguageLevels.NATIVE,
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name=related_name)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name=related_name)
    is_learning = models.BooleanField(default=False)
    is_speaking = models.BooleanField(default=False)
    language_level = models.PositiveSmallIntegerField(
        _("language level"), choices=LanguageLevels.choices, default=LanguageLevels.BEGINNER
    )

    def __str__(self):
        return f"{self.language.name} ({self.get_language_level_display()})"

    class Meta:
        indexes = (
            models.Index(fields=["language", "is_speaking"], name="language_speaking_idx"),
            models.Index(fields=["language", "is_learning"], name="language_learning_idx"),
        )
        constraints = (
            models.UniqueConstraint(
                fields=("user", "language"),
                name="unique_user_language",
                violation_error_message=_("A user_language record with such fields values already exists"),
            ),
        )

    @property
    def is_native(self):
        return self.is_speaking and self.language_level == LanguageLevels.NATIVE


class FeedbackMessage(models.Model):
    first_name = models.CharField(_("first_name"), max_length=250, null=True)
    email = models.CharField(_("email"), max_length=250)
    text = models.CharField(_("text"), max_length=250)
    processed = models.BooleanField(_("processed"), default=False)

    def __str__(self):
        return self.first_name or "-"

    class Meta:
        verbose_name = _("FeedbackMessage")
        verbose_name_plural = _("FeedbackMessages")
        ordering = ("first_name",)
