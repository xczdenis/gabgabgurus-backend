from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from gabgabgurus.api.v1.refs.serializers import NameSerializerResponse
from gabgabgurus.apps.hobbies.models import Hobby
from gabgabgurus.apps.languages.models import Country, Language


class BaseRefsListView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None
    serializer_class = NameSerializerResponse


class HobbyListView(BaseRefsListView):
    queryset = Hobby.objects.all()


class LanguageListView(BaseRefsListView):
    queryset = Language.objects.all()


class CountryListView(BaseRefsListView):
    queryset = Country.objects.all()
