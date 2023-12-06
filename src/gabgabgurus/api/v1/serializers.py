from django.contrib.auth import get_user_model
from rest_framework import serializers

from gabgabgurus.api.serializers import IDSerializer
from gabgabgurus.common.serializer_fields import DefaultImageField

User = get_user_model()


# class BaseUserResponse(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ("id", "email", "first_name", "avatar")


class BaseUserResponse(IDSerializer, serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    avatar = DefaultImageField(default="")
