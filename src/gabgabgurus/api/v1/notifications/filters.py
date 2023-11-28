from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from gabgabgurus.apps.chats.models import MessageStatus


class NotificationFilter(filters.FilterSet):
    status = filters.LookupChoiceFilter(
        label=_("Status"),
        field_name="status",
        lookup_choices=[
            ("exact", "Exact"),
            ("gt", "Grater than"),
            ("lt", "Less than"),
        ],
    )
    sender_id = filters.NumberFilter(field_name="message__sender", lookup_expr="exact")

    class Meta:
        model = MessageStatus
        fields = ("status",)
