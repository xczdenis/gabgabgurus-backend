import os
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.db.models import Manager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from PIL import Image

from gabgabgurus.apps.users.managers import CustomUserManager
from gabgabgurus.common.validators import MaxFileWeightValidator, MaxImageSizeValidator
from gabgabgurus.config.exceptions import EntityDoesntExist


def avatar_upload_to(instance, filename):
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    base, extension = os.path.splitext(filename)
    return f"users/{instance.id}/{base}_{now}{extension}"


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    AVATAR_MAX_WIDTH = 2600
    AVATAR_MAX_HEIGHT = 2600
    AVATAR_MAX_SIZE_B = 300 * 1024
    AVATAR_COMPRESS_QUALITY = 60

    username = None
    email = models.EmailField(_("email"), unique=True)
    avatar = models.ImageField(
        _("avatar"),
        upload_to=avatar_upload_to,
        default="",
        blank=True,
        validators=(
            MaxFileWeightValidator(AVATAR_MAX_SIZE_B),
            MaxImageSizeValidator(limit_width=AVATAR_MAX_WIDTH, limit_height=AVATAR_MAX_HEIGHT),
        ),
    )
    about_me = models.TextField(_("about me"), default="", blank=True, max_length=1000)
    country = models.ForeignKey("languages.Country", on_delete=models.SET_NULL, blank=True, null=True)
    hobbies = models.ManyToManyField("hobbies.Hobby", related_name="users", blank=True)
    blocked_users = models.ManyToManyField("User", related_name="blocked_by", blank=True)
    last_activity = models.DateTimeField(_("Last activity"), null=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        avatar_is_new = self.avatar_is_new()

        super().save(*args, **kwargs)

        if self.avatar and avatar_is_new:
            self.compress_avatar()

    def avatar_is_new(self):
        is_new = False
        if self.pk is not None:
            orig = User.objects.get(pk=self.pk)
            if orig.avatar != self.avatar:
                is_new = True
        else:
            is_new = True
        return is_new

    def compress_avatar(self):
        img = Image.open(self.avatar.path)
        img.save(self.avatar.path, quality=User.AVATAR_COMPRESS_QUALITY)

    def block_user(self, blocked_user: "User"):
        self.blocked_users.add(blocked_user)

    def unblock_user(self, blocked_user: "User"):
        self.blocked_users.remove(blocked_user)

    def is_blocked_user(self, user_id: int):
        return self.blocked_users.filter(id=user_id).exists()

    def update_from_kwargs(self, **kwargs) -> "User":
        with transaction.atomic():
            for field, value in kwargs.items():
                if hasattr(self, field):
                    field_instance = getattr(self, field)
                    if isinstance(field_instance, Manager):
                        field_instance.set(value)
                    else:
                        setattr(self, field, value)
            self.save()
        return self

    def delete_language(self, language):
        existing_user_languages = self.user_languages.filter(language=language)
        if not existing_user_languages:
            raise EntityDoesntExist("User does not have such a language")
        existing_user_languages.delete()

    def update_last_activity(self):
        User.objects.filter(id=self.id).update(last_activity=timezone.now())
