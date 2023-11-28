from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from gabgabgurus.config.settings.components.rest_auth import REFRESH_TOKEN_NAME

User = get_user_model()


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs[REFRESH_TOKEN_NAME] = self.context["request"].COOKIES.get(REFRESH_TOKEN_NAME)
        if attrs[REFRESH_TOKEN_NAME]:
            return super().validate(attrs)
        else:
            raise InvalidToken(f"No valid token found in cookie '{REFRESH_TOKEN_NAME}'")


class UserCreationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
