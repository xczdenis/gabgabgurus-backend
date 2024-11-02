from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from gabgabgurus.api.serializers import IDSerializer, PageNumberQueryParamsSerializer
from gabgabgurus.apps.hobbies.models import Hobby
from gabgabgurus.apps.languages.models import Country, Language
from gabgabgurus.common.serializer_fields import DefaultImageField, ListJsonField, TimestampField
from gabgabgurus.common.utils.models import get_validators

User = get_user_model()


class UserLanguageResponse(serializers.Serializer):
    language = serializers.StringRelatedField()
    language_level = serializers.IntegerField()


class MemberListQueryParams(PageNumberQueryParamsSerializer, serializers.Serializer):
    speaks = ListJsonField(
        help_text=_("List of languages spoken by the interlocutor"),
        required=False,
    )
    learning = ListJsonField(
        help_text=_("List of languages that the interlocutor is learning"),
        required=False,
    )
    countries = ListJsonField(
        help_text=_("List of user's countries"),
        required=False,
    )
    hobbies = ListJsonField(
        help_text=_("List of user's hobbies"),
        required=False,
    )
    top = serializers.IntegerField(
        help_text=_("Number of TOP users"),
        required=False,
    )


class MemberBaseResponse(IDSerializer, serializers.Serializer):
    first_name = serializers.CharField()
    email = serializers.EmailField()
    country = serializers.StringRelatedField(default="")
    avatar = DefaultImageField(default="")
    about_me = serializers.CharField()
    hobbies = serializers.StringRelatedField(many=True)
    speaks = UserLanguageResponse(many=True)
    learning = UserLanguageResponse(many=True)
    last_activity = TimestampField()


class MemberListResponse(MemberBaseResponse, serializers.Serializer):
    pass


class MemberDetailResponse(MemberBaseResponse, serializers.Serializer):
    is_blocked = serializers.BooleanField(default=False)
    blocked_for = serializers.BooleanField(default=False)


class MyProfileResponse(IDSerializer, serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    country = serializers.StringRelatedField()
    about_me = serializers.CharField()
    avatar = DefaultImageField(default="")
    hobbies = serializers.StringRelatedField(many=True)
    speaks = UserLanguageResponse(many=True)
    learning = UserLanguageResponse(many=True)


class MyProfileRequest(serializers.Serializer):
    first_name = serializers.CharField()
    country = serializers.SlugRelatedField(queryset=Country.objects.all(), slug_field="name")
    about_me = serializers.CharField(allow_blank=True)
    hobbies = serializers.SlugRelatedField(queryset=Hobby.objects.all(), slug_field="name", many=True)


class MyAvatarRequest(serializers.Serializer):
    avatar = Base64ImageField(validators=get_validators(User, "avatar"))


class MyLanguagesResponse(serializers.Serializer):
    language = serializers.StringRelatedField()
    language_level = serializers.IntegerField()
    is_speaking = serializers.BooleanField()
    is_learning = serializers.BooleanField()


class MyLanguagesRequest(serializers.Serializer):
    language = serializers.SlugRelatedField(queryset=Language.objects.all(), slug_field="name")
    language_level = serializers.IntegerField(min_value=0, max_value=5, required=False)
    is_speaking = serializers.BooleanField(required=False)
    is_learning = serializers.BooleanField(required=False)


class MyBlockedUsersResponse(IDSerializer, serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()


class MyBlockedUsersRequest(serializers.Serializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="id")


class FeedbackRequest(serializers.Serializer):
    first_name = serializers.CharField()
    email = serializers.CharField()
    text = serializers.CharField()


class FeedbackResponse(serializers.Serializer):
    first_name = serializers.CharField()
    email = serializers.CharField()
    text = serializers.CharField()
    processed = serializers.BooleanField()
