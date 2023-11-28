from rest_framework import serializers


class NameSerializerResponse(serializers.Serializer):
    name = serializers.StringRelatedField()
