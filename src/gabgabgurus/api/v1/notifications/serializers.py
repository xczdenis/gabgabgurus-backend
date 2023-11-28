from django.contrib.auth import get_user_model
from rest_framework import serializers

from gabgabgurus.api.serializers import IDSerializer
from gabgabgurus.apps.chats.enums import MessageStatuses
from gabgabgurus.common.serializer_fields import DefaultImageField, TimestampField

User = get_user_model()


class MessageSenderSerializer(IDSerializer, serializers.Serializer):
    first_name = serializers.CharField()
    avatar = DefaultImageField(default="")
    last_activity = TimestampField()
    # last_activity = serializers.SerializerMethodField()
    #
    # def get_last_activity(self, obj):
    #     return get_user_last_activity_timestamp_from_cache(obj)


class MessageSerializer(IDSerializer, serializers.Serializer):
    text = serializers.CharField()
    sender = MessageSenderSerializer(many=False)


class NotificationResponse(IDSerializer, serializers.Serializer):
    message = MessageSerializer(many=False)
    status = serializers.CharField()
    created_at = TimestampField()
    is_read = serializers.BooleanField()


class NotificationRequest(serializers.Serializer):
    status = serializers.ChoiceField(choices=MessageStatuses.choices, required=True)
