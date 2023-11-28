from django_filters import rest_framework as filters

from gabgabgurus.apps.chats.models import Message


class MessageListFilter(filters.FilterSet):
    channel_id = filters.NumberFilter(field_name="channel__id", lookup_expr="exact", required=True)

    class Meta:
        model = Message
        fields = ("channel",)
