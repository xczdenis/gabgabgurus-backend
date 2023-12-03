"""
ASGI config for gabgabgurus project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gabgabgurus.config.settings")

asgi_app = get_asgi_application()

# In order to import websocket_urlpatterns from gabgabgurus.config.urls
# we need to call django.setup() - this is called in get_asgi_application() function.
# This is why we put import at here
from gabgabgurus.config.urls import websocket_urlpatterns  # noqa E402

application = ProtocolTypeRouter(
    {
        "http": asgi_app,
        "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(websocket_urlpatterns))),
    }
)
