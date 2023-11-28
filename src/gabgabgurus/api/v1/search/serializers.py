# from django.contrib.auth import get_user_model
# from django.utils.translation import gettext_lazy as _
# from rest_framework import serializers
#
# from gabgabgurus.api.fields import ListJsonSlugRelatedField
# from gabgabgurus.apps.hobbies.models import Hobby
# from gabgabgurus.apps.languages.models import Language, Country
# from gabgabgurus.apps.user_details.models import UserLanguage
#
# User = get_user_model()
#
#
# class InterlocutorListQueryParamsSerializer(serializers.Serializer):
#     page = serializers.IntegerField(help_text=_("Page number"), required=False, min_value=1)
#     count = serializers.IntegerField(
#         help_text=_("Items on page"),
#         required=False,
#         min_value=1,
#     )
#     speaks = ListJsonSlugRelatedField(
#         help_text=_("List of languages spoken by the interlocutor"),
#         required=False,
#         queryset=Language.objects.all(),
#         slug_field="",
#     )
#     learning = ListJsonSlugRelatedField(
#         help_text=_("List of languages that the interlocutor is learning"),
#         required=False,
#         queryset=Language.objects.all(),
#         slug_field="",
#     )
#     countries = ListJsonSlugRelatedField(
#         help_text=_("List of user's countries"),
#         required=False,
#         queryset=Country.objects.all(),
#         slug_field="",
#     )
#     hobbies = ListJsonSlugRelatedField(
#         help_text=_("List of user's hobbies"),
#         required=False,
#         queryset=Hobby.objects.all(),
#         slug_field="",
#     )
#
#
# class InterlocutorListSerializer(serializers.ModelSerializer):
#     class NestedUserLanguageSerializer(serializers.ModelSerializer):
#         language = serializers.StringRelatedField(many=False)
#
#         class Meta:
#             model = UserLanguage
#             fields = ("language", "language_level")
#
#     country = serializers.StringRelatedField(many=False)
#     hobbies = serializers.StringRelatedField(many=True)
#     speaks = NestedUserLanguageSerializer(many=True)
#     learning = NestedUserLanguageSerializer(many=True)
#     avatar = serializers.ImageField(read_only=True)
#
#     class Meta:
#         model = User
#         fields = (
#             "id",
#             "first_name",
#             "country",
#             "about_me",
#             "speaks",
#             "learning",
#             "hobbies",
#             "avatar",
#         )
