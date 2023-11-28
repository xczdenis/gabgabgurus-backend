from django.urls import path

from gabgabgurus.api.v1.refs.views import CountryListView, HobbyListView, LanguageListView

app_name = "refs"

urlpatterns = [
    path("hobbies/", HobbyListView.as_view(), name="hobbies"),
    path("countries/", CountryListView.as_view(), name="countries"),
    path("languages/", LanguageListView.as_view(), name="languages"),
]
