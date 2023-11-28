from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from gabgabgurus.api.v1.fake.services.countries import generate_countries
from gabgabgurus.api.v1.fake.services.languages import generate_languages
from gabgabgurus.api.v1.fake.services.user_language import generate_user_language
from gabgabgurus.api.v1.fake.services.users import generate_users
from gabgabgurus.apps.languages.models import Country, Language
from gabgabgurus.apps.user_details.models import UserLanguage

User = get_user_model()


class Generator(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        response_data = {}

        n_users = request.data.get("users") or 0
        n_countries = request.data.get("countries") or 0
        n_languages = request.data.get("languages") or 0
        ul = request.data.get("ul") or 0

        if n_users:
            response_data["users"] = {
                "created": generate_users(n_users),
                "total": User.objects.count(),
            }
        if n_countries:
            response_data["countries"] = {
                "created": generate_countries(n_countries),
                "total": Country.objects.count(),
            }
        if n_languages:
            response_data["languages"] = {
                "created": generate_languages(n_languages),
                "total": Language.objects.count(),
            }
        if ul:
            response_data["ul"] = {
                "created": generate_user_language(ul),
                "total": UserLanguage.objects.count(),
            }

        return Response(response_data)
