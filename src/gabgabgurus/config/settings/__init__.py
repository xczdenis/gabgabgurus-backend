from split_settings.tools import include, optional

from gabgabgurus.config import app_config

_base_settings = (
    "components/base.py",
    "components/cache.py",
    "components/channels.py",
    "components/database.py",
    "components/drf.py",
    "components/openapi.py",
    "components/oauth.py",
    "components/rest_auth.py",
    "components/simplejwt.py",
    # Select the right env:
    "environments/{0}.py".format(app_config.ENVIRONMENT),
    # Optionally override some settings:
    optional("environments/local.py"),
)

include(*_base_settings)
