from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from gabgabgurus.api.v1.chats.serializers import channels, messages, user_channels
from gabgabgurus.apps.chats.selectors import get_channels, get_user_channel_messages, get_user_channels
from gabgabgurus.apps.chats.services.db import (
    create_channel,
    create_message,
    create_user_channels,
    filter_channels_queryset,
    mark_messages_as_read,
)
from gabgabgurus.common.mixins.view import ExtendedCreateAPIView
from gabgabgurus.common.utils.api import get_validated_data


class ChannelListCreateView(ExtendedCreateAPIView, ListAPIView):
    serializer_class = channels.ChannelResponse
    input_serializer_class = channels.ChannelRequest
    output_serializer_class = channels.ChannelResponse

    def get_queryset(self):
        return get_channels(owner=self.request.user)

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        validated_data["owner"] = self.request.user
        return create_channel(**validated_data)


class UserChannelListCreateView(ExtendedCreateAPIView, ListAPIView):
    serializer_class = user_channels.UserChannelResponse
    input_serializer_class = user_channels.UserChannelRequest
    query_params_serializer_class = user_channels.UserChannelQuery

    def get_queryset(self):
        queryset = get_user_channels(self.request.user)
        queryset = self.filter_queryset_by_query_params(queryset)
        return queryset

    def filter_queryset_by_query_params(self, queryset):
        query_params = self.parse_query_params_to_dict()

        participants_ids = query_params.get("participants")
        if participants_ids:
            participants_ids.append(self.request.user.id)

            queryset = filter_channels_queryset(
                queryset=queryset,
                related_field="channel",
                participants=participants_ids,
                channel_type=query_params.get("channel_type"),
            )

        return queryset

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        member_ids = validated_data["member_ids"]
        member_ids.append(self.request.user.id)
        return create_user_channels(member_ids, validated_data["channel"])


class MessageListCreateView(ExtendedCreateAPIView, ListAPIView):
    serializer_class = messages.MessageResponse
    input_serializer_class = messages.MessageRequest
    output_serializer_class = messages.MessageResponse
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        channel_id = self.kwargs.get("channel_id")
        return get_user_channel_messages(self.request.user, channel=channel_id, statuses=True)

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        validated_data["sender"] = self.request.user
        return create_message(**validated_data)


class MessagesMarkAsReadView(GenericAPIView):
    serializer_class = messages.MarkMessagesAsReadRequest

    def patch(self, request, *args, **kwargs):
        validated_data = get_validated_data(self.get_serializer_class(), request.data)
        mark_messages_as_read(**validated_data)
        return Response({}, status=status.HTTP_200_OK)
