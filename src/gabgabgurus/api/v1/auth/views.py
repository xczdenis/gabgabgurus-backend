from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenViewBase

from gabgabgurus.api.v1.auth.serializers import CookieTokenRefreshSerializer, UserCreationSerializer
from gabgabgurus.api.v1.serializers import BaseUserResponse
from gabgabgurus.apps.users.services import create_user_if_not_exists, update_user_last_login
from gabgabgurus.config.settings.components.rest_auth import ACCESS_TOKEN_NAME, REFRESH_TOKEN_NAME

User = get_user_model()


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        input_serializer = UserCreationSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user = create_user_if_not_exists(**input_serializer.validated_data)

        output_serializer = BaseUserResponse(user)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class CookieTokenViewBase(TokenViewBase):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        if hasattr(serializer, "user"):
            serializer.validated_data["user"] = BaseUserResponse(serializer.user).data

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    def finalize_response(self, request, response, *args, **kwargs):
        for token_type, token_lifetime_seconds in self.get_tokens().items():
            self.set_token_from_response_to_cookie(response, token_type, token_lifetime_seconds)
        return super().finalize_response(request, response, *args, **kwargs)

    @classmethod
    def get_tokens(cls):
        return {
            ACCESS_TOKEN_NAME: int(api_settings.ACCESS_TOKEN_LIFETIME.total_seconds()),
            REFRESH_TOKEN_NAME: int(api_settings.REFRESH_TOKEN_LIFETIME.total_seconds()),
        }

    def set_token_from_response_to_cookie(self, response, token_type, cookie_max_age):
        token = response.data.get(token_type)
        if token:
            self.set_cookie(response, token_type, token, cookie_max_age)
            self.del_key_from_response(response, token_type)

    @classmethod
    def set_cookie(cls, response, key, value, max_age):
        response.set_cookie(key, value, max_age=max_age, httponly=True, samesite="None", secure=False)

    @classmethod
    def del_key_from_response(cls, response, key):
        del response.data[key]


class SignInView(CookieTokenViewBase, TokenObtainPairView):
    permission_classes = [AllowAny]


class CookieTokenRefreshView(CookieTokenViewBase, TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        self.update_user_last_login_view(response)
        return response

    def update_user_last_login_view(self, response):
        user_id = self.get_user_id_from_response(response)
        if user_id is not None:
            update_user_last_login(user_id)

    @classmethod
    def get_user_id_from_response(cls, response):
        refresh_token_str = response.data.get(REFRESH_TOKEN_NAME)
        if refresh_token_str:
            token = RefreshToken(refresh_token_str)
            return token.payload.get("user_id")
        return None
