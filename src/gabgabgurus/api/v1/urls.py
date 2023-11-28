from importlib import import_module

from channels.routing import URLRouter
from django.conf import settings
from django.urls import include, path

from gabgabgurus.config.api_config import APIVersions

app_name = APIVersions.V1.value


def make_path(package_name: str, url: str = ""):
    return path("{url}/".format(url=url or package_name), make_include(package_name))


def make_include(package_name: str):
    return include("api.v1.{package}.urls".format(package=package_name))


api_packages = [
    "auth",
    "chats",
    "notifications",
    "oauth",
    "refs",
    "users",
]
if settings.DEBUG:
    api_packages.append("fake")

urlpatterns = [make_path(package_name) for package_name in api_packages]

websocket_urlpatterns = []
for package_name in api_packages:
    module = import_module(f"api.v1.{package_name}.urls")
    package_websocket_urlpatterns = getattr(module, "websocket_urlpatterns", None)
    if package_websocket_urlpatterns:
        websocket_urlpatterns += [
            path("{url}/".format(url=package_name), URLRouter(package_websocket_urlpatterns)),
        ]
