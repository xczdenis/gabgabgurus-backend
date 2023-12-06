from gabgabgurus.config.settings.components.base import MIDDLEWARE
from gabgabgurus.config.settings.utils import add_to_collection

SOCIALACCOUNT_PROVIDERS = {
    "github": {
        "OAUTH_PKCE_ENABLED": True,
    },
}

SITE_ID = 1

add_to_collection("allauth.account.middleware.AccountMiddleware", MIDDLEWARE)

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = None
