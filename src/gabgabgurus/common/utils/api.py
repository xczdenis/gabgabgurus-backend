from typing import Type

from rest_framework.serializers import Serializer
from rest_framework.settings import api_settings


def get_success_headers(data):
    try:
        return {"Location": str(data[api_settings.URL_FIELD_NAME])}
    except (TypeError, KeyError):
        return {}


def get_validated_data(serializer_class: Type[Serializer], data, **kwargs):
    raise_exception = kwargs.pop("raise_exception", True)
    serializer = serializer_class(data=data, **kwargs)
    serializer.is_valid(raise_exception=raise_exception)
    return serializer.validated_data
