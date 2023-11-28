from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class PageNumberQueryParamsSerializer(serializers.Serializer):
    page = serializers.IntegerField(help_text=_("Page number"), required=False, min_value=1)
    count = serializers.IntegerField(
        help_text=_("Items on page"),
        required=False,
        min_value=1,
    )


class LimitOffsetQueryParamsSerializer(serializers.Serializer):
    limit = serializers.IntegerField(
        help_text=_(
            "Indicates the maximum number of items to return, "
            "and is equivalent to the page_size in other styles."
        ),
        required=False,
        min_value=1,
    )
    offset = serializers.IntegerField(
        help_text=_(
            "indicates the starting position of the query in relation to "
            "the complete set of unpaginated items."
        ),
        required=False,
        min_value=0,
    )


class IDSerializer(serializers.Serializer):
    id = serializers.IntegerField()
