from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class BaseUserResponse(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "avatar")
