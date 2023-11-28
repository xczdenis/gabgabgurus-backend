from rest_framework import serializers

from gabgabgurus.api.serializers import IDSerializer
from gabgabgurus.common.serializer_fields import TimestampField


class ChannelRequest(serializers.Serializer):
    pass


class ChannelResponse(IDSerializer, serializers.Serializer):
    owner = serializers.EmailField(source="owner.email")
    created_at = TimestampField()
