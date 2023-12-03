from channels.routing import URLRouter
from django.urls import include, path

from gabgabgurus.api.v1.urls import websocket_urlpatterns as websocket_urlpatterns_v1
from gabgabgurus.config.api_config import APIVersions

app_name = "api"

urlpatterns = [
    path(f"{APIVersions.V1.value}/", include("gabgabgurus.api.v1.urls", namespace=APIVersions.V1.value)),
]

websocket_urlpatterns = [
    path(f"{APIVersions.V1.value}/", URLRouter(websocket_urlpatterns_v1)),
]
