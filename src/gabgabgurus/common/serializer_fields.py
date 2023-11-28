import urllib.parse
from json import JSONDecodeError

import orjson
from rest_framework import serializers


class ListJsonBaseField(serializers.Field):
    def to_internal_value(self, data):
        decoded_data = self.decode_data(data)
        pure_value_list = self.parse_json_data(decoded_data)
        return self.finalize_internal_value(pure_value_list)

    def decode_data(self, data):
        try:
            return urllib.parse.unquote(data)
        except (ValueError, TypeError):
            raise serializers.ValidationError(f"Invalid format for {self.field_name} field")

    def parse_json_data(self, data):
        try:
            parsed_data = orjson.loads(data)
        except JSONDecodeError:
            parsed_data = data
        except Exception:
            raise serializers.ValidationError(f"Invalid json data for {self.field_name} field")
        if not isinstance(parsed_data, list):
            parsed_data = [parsed_data]
        return parsed_data

    @classmethod
    def finalize_internal_value(cls, decoded_internal_value):
        return decoded_internal_value

    def to_representation(self, value_list):
        return [str(value) for value in value_list]


class ListJsonField(ListJsonBaseField, serializers.CharField):
    pass


class ListJsonSlugRelatedField(ListJsonBaseField, serializers.SlugRelatedField):
    def finalize_internal_value(self, decoded_internal_value):
        if self.queryset is not None and self.slug_field is not None:
            filtered_queryset = self.filter_queryset(decoded_internal_value)
            return filtered_queryset.all()

    def filter_queryset(self, value_list):
        filter_key = "{}__in".format(self.slug_field)
        return self.queryset.filter(**{filter_key: value_list})

    def to_representation(self, value_list):
        return [getattr(value, self.slug_field) for value in value_list]


class TimestampField(serializers.Field):
    def to_representation(self, value):
        return value.timestamp()


class DefaultImageField(serializers.ImageField):
    def to_representation(self, value):
        if not value:
            return self.default if self.default is not None else None
        return super().to_representation(value)
