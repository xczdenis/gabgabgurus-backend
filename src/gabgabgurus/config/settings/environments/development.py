"""
This file contains all the settings that defines the development server.
SECURITY WARNING: don't run with debug turned on in production!
"""

import socket

from loguru import logger

from gabgabgurus.config.settings.components.base import INSTALLED_APPS, MIDDLEWARE
from gabgabgurus.config.settings.utils import add_to_collection

# Setting the development status:
DEBUG = True


def custom_show_toolbar(request) -> bool:
    """Only show the debug toolbar to users with the superuser flag."""
    return DEBUG and (request.META["REMOTE_ADDR"] in INTERNAL_IPS and request.user.is_superuser)


def get_list_of_ip_for_host() -> list[str]:
    """
    Returns list of IP addresses for a host.
    The host argument is a string giving a host name or IP number
    """
    list_of_ip = []

    current_host_name = socket.gethostname()
    try:
        hostname, aliases, list_of_ip = socket.gethostbyname_ex(current_host_name)
    except Exception as e:
        logger.error("Can't get a list of IP for host {}: {}", current_host_name, e)

    return list_of_ip


# Installed apps for development only:
add_to_collection("debug_toolbar", INSTALLED_APPS)

# Django debug toolbar:
# https://django-debug-toolbar.readthedocs.io
add_to_collection("debug_toolbar.middleware.DebugToolbarMiddleware", MIDDLEWARE)

# https://django-debug-toolbar.readthedocs.io/en/stable/installation.html#configure-internal-ips
# ips = get_list_of_ip_for_host()
# INTERNAL_IPS = ["{0}.1".format(ip[: ip.rfind(".")]) for ip in ips]
INTERNAL_IPS = ["127.0.0.1"]

DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": custom_show_toolbar}

# Security
# https://docs.djangoproject.com/en/dev/topics/security/
SECURE_CROSS_ORIGIN_OPENER_POLICY = None
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
