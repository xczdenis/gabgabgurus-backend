import debug_toolbar
from channels.routing import URLRouter
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from gabgabgurus.api.urls import websocket_urlpatterns
from gabgabgurus.config.api_config import api_config

# pages
urlpatterns = [
    path("api/admin/", admin.site.urls),
]

# REST API
urlpatterns += [
    path(f"{api_config.base_path}/", include("gabgabgurus.api.urls")),
    path(f"{api_config.openapi_path}/", SpectacularAPIView.as_view(), name="openapi"),
    path(f"{api_config.swagger_path}/", SpectacularSwaggerView.as_view(url_name="openapi"), name="swagger"),
    path(f"{api_config.redoc_path}/", SpectacularRedocView.as_view(url_name="openapi"), name="redoc"),
]

# Websockets
websocket_urlpatterns = [
    path(f"ws/{api_config.base_path}/", URLRouter(websocket_urlpatterns)),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
