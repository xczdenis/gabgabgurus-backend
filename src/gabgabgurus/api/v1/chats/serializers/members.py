from rest_framework import serializers

from gabgabgurus.api.serializers import IDSerializer
from gabgabgurus.common.serializer_fields import DefaultImageField, TimestampField


class ChannelMemberResponse(IDSerializer, serializers.Serializer):
    first_name = serializers.CharField()
    avatar = DefaultImageField(default="")
    last_login = TimestampField()
    is_blocked = serializers.BooleanField()
    blocked_for = serializers.BooleanField()
