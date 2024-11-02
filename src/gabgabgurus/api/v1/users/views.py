from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from gabgabgurus.api.v1.serializers import BaseUserResponse
from gabgabgurus.api.v1.users import serializers
from gabgabgurus.apps.user_details.models import FeedbackMessage
from gabgabgurus.apps.user_details.selectors import annotate_user_languages_with_relations
from gabgabgurus.apps.user_details.services import create_feedback_message, create_update_user_language
from gabgabgurus.apps.users.selectors import annotate_user_queryset_with_relations, get_top_users, get_users
from gabgabgurus.common.mixins.view import (
    ExtendedUpdateAPIView,
    InputOutputSerializerAPIView,
    QueryParamsMixin,
)
from gabgabgurus.common.utils.api import get_validated_data

User = get_user_model()


@method_decorator(ensure_csrf_cookie, name="dispatch")
class IAmView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = BaseUserResponse

    def get_object(self):
        return self.request.user


@extend_schema(parameters=[serializers.MemberListQueryParams])
class MemberListView(QueryParamsMixin, ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = serializers.MemberListResponse
    query_params_serializer_class = serializers.MemberListQueryParams

    def get_queryset(self):
        query_params = self.parse_query_params_to_dict()

        top_users_count = query_params.get("top") or 0
        if top_users_count > 0:
            return get_top_users(top_users_count)

        lookup_field = "name"
        qs = get_users(
            speaks=query_params.get("speaks"),
            speaks_lookup=lookup_field,
            learning=query_params.get("learning"),
            learning_lookup=lookup_field,
            countries=query_params.get("countries"),
            countries_lookup=lookup_field,
            hobbies=query_params.get("hobbies"),
            hobbies_lookup=lookup_field,
        )
        return qs.all()


class MemberDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = serializers.MemberDetailResponse

    def get_queryset(self):
        qs = super().get_queryset()
        blocker = self.request.user if self.request.user.is_authenticated else None
        qs = annotate_user_queryset_with_relations(qs, blocker=blocker)
        return qs


class UserLastActivityView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.request.user.update_last_activity()
        return Response({})


class MyProfileView(ExtendedUpdateAPIView, RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.MyProfileResponse
    input_serializer_class = serializers.MyProfileRequest
    output_serializer_class = serializers.MyProfileResponse
    http_method_names = ["get", "patch", "head", "options"]

    def get_queryset(self):
        self.kwargs["pk"] = self.request.user.pk
        qs = super().get_queryset()
        return annotate_user_queryset_with_relations(qs)

    def perform_update(self, serializer):
        validated_data = serializer.validated_data
        self.request.user.update_from_kwargs(**validated_data)
        return self.get_object()


class MyAvatarUpdateView(UpdateAPIView):
    serializer_class = serializers.MyAvatarRequest
    http_method_names = ["patch", "delete", "head", "options"]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = self.request.user
        user.avatar = serializer.validated_data["avatar"]
        user.save()

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.avatar = ""
        user.save()
        return Response({})


class MyLanguagesUpdateView(InputOutputSerializerAPIView, ListAPIView):
    serializer_class = serializers.MyLanguagesResponse
    input_serializer_class = serializers.MyLanguagesRequest
    output_serializer_class = serializers.MyLanguagesResponse
    pagination_class = None

    def get_queryset(self):
        qs = self.request.user.user_languages
        return annotate_user_languages_with_relations(qs)

    def post(self, request, *args, **kwargs):
        validated_data = get_validated_data(self.get_serializer_class(), request.data)
        user_language = create_update_user_language(self.request.user, validated_data)
        output_serializer_class = self.get_output_serializer_class()
        output_serializer = output_serializer_class(user_language)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        validated_data = get_validated_data(self.get_serializer_class(), request.data)
        self.request.user.delete_language(validated_data["language"])
        return Response({})


class MyBlockedUsersUpdateView(InputOutputSerializerAPIView, ListAPIView):
    serializer_class = serializers.MyBlockedUsersResponse
    input_serializer_class = serializers.MyBlockedUsersRequest
    output_serializer_class = serializers.MyBlockedUsersResponse
    pagination_class = None

    def get_queryset(self):
        qs = self.request.user.blocked_users.order_by("pk")
        return qs

    def post(self, request, *args, **kwargs):
        validated_data = get_validated_data(self.get_serializer_class(), request.data)
        self.request.user.block_user(validated_data["user"])
        return Response({})

    def delete(self, request, *args, **kwargs):
        validated_data = get_validated_data(self.get_serializer_class(), request.data)
        self.request.user.unblock_user(validated_data["user"])
        return Response({})


class FeedbackView(InputOutputSerializerAPIView, ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = serializers.FeedbackResponse
    input_serializer_class = serializers.FeedbackRequest
    output_serializer_class = serializers.FeedbackResponse

    def get_queryset(self):
        return FeedbackMessage.objects.all().filter(processed=False)

    def post(self, request, *args, **kwargs):
        validated_data = get_validated_data(self.get_serializer_class(), request.data)
        feedback_message = create_feedback_message(validated_data)
        output_serializer_class = self.get_output_serializer_class()
        output_serializer = output_serializer_class(feedback_message)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
