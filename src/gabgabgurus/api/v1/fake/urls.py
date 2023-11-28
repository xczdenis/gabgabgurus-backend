from django.urls import path
from rest_framework import routers

from gabgabgurus.api.v1.fake import views

app_name = "fake"

router = routers.DefaultRouter()

urlpatterns = [
    path("all/", views.Generator.as_view(), name="fake"),
]
