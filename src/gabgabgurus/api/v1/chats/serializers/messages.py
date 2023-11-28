from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from gabgabgurus.api.serializers import IDSerializer
from gabgabgurus.apps.chats.models import Message
from gabgabgurus.common.serializer_fields import DefaultImageField, TimestampField


class MessageRequest(serializers.Serializer):
    channel_id = serializers.IntegerField(
        help_text=_("Channel id"),
        required=True,
        write_only=True,
    )
    text = serializers.CharField(
        help_text=_("Message text"),
        required=True,
        min_length=1,
        max_length=Message.TEXT_MAX_LENGTH,
    )


class MarkMessagesAsReadRequest(serializers.Serializer):
    message_ids = serializers.ListField(child=serializers.IntegerField(), required=True, write_only=True)
    recipient_id = serializers.IntegerField(required=True, write_only=True)


class MessageAuthorResponse(IDSerializer, serializers.Serializer):
    first_name = serializers.CharField()
    avatar = DefaultImageField(default="")


class MessageStatusUserResponse(IDSerializer):
    first_name = serializers.CharField()


class MessageStatusResponse(serializers.Serializer):
    status = serializers.IntegerField()
    user = MessageStatusUserResponse()


class MessageResponse(IDSerializer, serializers.Serializer):
    text = serializers.CharField()
    created_at = TimestampField()
    sender = MessageAuthorResponse(many=False)
    status = serializers.IntegerField()
