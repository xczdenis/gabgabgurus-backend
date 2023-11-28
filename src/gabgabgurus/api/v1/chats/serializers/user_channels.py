from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from gabgabgurus.api.serializers import PageNumberQueryParamsSerializer
from gabgabgurus.api.v1.chats.serializers.members import ChannelMemberResponse
from gabgabgurus.apps.chats.models import Channel
from gabgabgurus.common.serializer_fields import ListJsonField, TimestampField


class UserChannelQuery(PageNumberQueryParamsSerializer, serializers.Serializer):
    participants = ListJsonField(
        help_text=_("List of participants ids"),
        required=False,
        default=[],
    )
    channel_type = serializers.IntegerField(
        help_text=_("Channel type"),
        required=False,
    )


class UserChannelRequest(serializers.Serializer):
    channel = serializers.SlugRelatedField(
        queryset=Channel.objects.all(),
        slug_field="id",
        required=True,
        write_only=True,
    )
    member_ids = serializers.ListSerializer(child=serializers.IntegerField(), required=True, write_only=True)


class UserChannelResponse(serializers.Serializer):
    id = serializers.IntegerField(source="channel.id")
    last_activity = TimestampField()
    unread_count = serializers.IntegerField()
    last_message = serializers.CharField()
    participants = ChannelMemberResponse(source="channel.participants", many=True)
