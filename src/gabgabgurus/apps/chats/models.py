from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from gabgabgurus.apps.chats.enums import ChannelTypes, MessageStatuses
from gabgabgurus.common.mixins.models import CreatedAtMixin, TimeStampedMixin
from gabgabgurus.common.utils.models import bulk_create

User = get_user_model()


class Channel(CreatedAtMixin, models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="chats", null=True)
    participants = models.ManyToManyField(User, through="UserChannel")
    channel_type = models.PositiveSmallIntegerField(
        _("channel type"), choices=ChannelTypes.choices, default=ChannelTypes.PRIVATE
    )

    def __str__(self):
        return f"Channel #{self.pk} - {self.owner.email}" if self.owner else f"{self.pk}"

    class Meta:
        verbose_name = _("Channel")
        verbose_name_plural = _("Channels")
        ordering = ("-id",)

    def is_available_for_user(self, user: User):
        return self.participants.filter(id=user.id).exists()


class UserChannel(CreatedAtMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_channels")
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="user_channels")

    class Meta:
        verbose_name = _("User channel")
        verbose_name_plural = _("User channels")
        constraints = (
            models.UniqueConstraint(
                fields=("user", "channel"),
                name="unique_user_channel",
                violation_error_message=_("A user_channel record with such fields values already exists"),
            ),
        )


class Message(TimeStampedMixin, models.Model):
    TEXT_MAX_LENGTH = 2000

    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="sent_messages", null=True)
    text = models.TextField(_("text"), default="", max_length=TEXT_MAX_LENGTH)

    def __str__(self):
        return f"{self.text[:30]} from {self.sender.email}"

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def create_message_statuses(
        self, recipients: QuerySet[User], status: MessageStatuses = MessageStatuses.CREATED
    ):
        new_objs = (MessageStatus(user=recipient, message=self, status=status) for recipient in recipients)
        return bulk_create(MessageStatus, new_objs)


class MessageStatus(TimeStampedMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_statuses")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="message_statuses")
    status = models.PositiveSmallIntegerField(
        _("status"), choices=MessageStatuses.choices, default=MessageStatuses.CREATED
    )

    class Meta:
        verbose_name = _("Message status")
        verbose_name_plural = _("Message statuses")
        constraints = (
            models.UniqueConstraint(
                fields=("user", "message"),
                name="unique_user_message",
                violation_error_message=_("A user_message record with such fields values already exists"),
            ),
        )
