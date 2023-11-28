from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from gabgabgurus.api.v1.notifications import serializers
from gabgabgurus.api.v1.notifications.filters import NotificationFilter
from gabgabgurus.apps.chats.models import MessageStatus
from gabgabgurus.apps.chats.selectors import get_message_statuses
from gabgabgurus.common.mixins.view import ExtendedUpdateAPIView, InputOutputSerializerAPIView
from gabgabgurus.common.utils.api import get_validated_data
from gabgabgurus.common.utils.models import bulk_update_objects_from_data, update_object_from_kwargs

User = get_user_model()


class NotificationListUpdateView(InputOutputSerializerAPIView, ListAPIView):
    serializer_class = serializers.NotificationResponse
    input_serializer_class = serializers.NotificationRequest
    queryset = get_message_statuses(add_is_read=True)
    filterset_class = NotificationFilter
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    def patch(self, request, *args, **kwargs):
        filtered_queryset = self.filter_queryset(self.get_queryset())
        validated_data = get_validated_data(self.get_serializer_class(), request.data)
        bulk_update_objects_from_data(MessageStatus, filtered_queryset, data=validated_data)
        return Response({})


class NotificationUpdateView(ExtendedUpdateAPIView):
    serializer_class = serializers.NotificationResponse
    input_serializer_class = serializers.NotificationRequest
    output_serializer_class = serializers.NotificationResponse

    def get_queryset(self):
        qs = get_message_statuses(add_is_read=True)
        qs = qs.filter(user=self.request.user)
        return qs

    def perform_update(self, serializer):
        update_object_from_kwargs(self.get_object(), **serializer.validated_data)
        return self.get_object()
