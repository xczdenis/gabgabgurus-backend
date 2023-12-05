from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.providers.base import AuthAction
from allauth.socialaccount.providers.github.provider import GitHubProvider
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.views import LogoutView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from loguru import logger

from gabgabgurus.api.v1.serializers import BaseUserResponse
from gabgabgurus.config import oauth2_config
from gabgabgurus.config.settings.components.rest_auth import ACCESS_TOKEN_NAME, REFRESH_TOKEN_NAME

User = get_user_model()


class OAuth2LoginView(SocialLoginView):
    callback_url = oauth2_config.REDIRECT_URI
    client_class = OAuth2Client
    adapter_class = OAuth2Adapter

    def dispatch(self, *args, **kwargs):
        # session_key = self.request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        # logger.info(f"dispatch. session_key = {session_key}")

        # oauth2_provider = self.request.session.get("oauth2_provider")
        # logger.info(f"dispatch. oauth2_provider = {oauth2_provider}")

        self.set_adapter()
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        # logger.info(f"get. settings.SESSION_COOKIE_NAME = {settings.SESSION_COOKIE_NAME}")

        # test_key = request.session.get("test_key")
        # logger.info(f"get. get-test-key = {test_key}")

        # oauth2_provider = request.session.get("oauth2_provider")
        # logger.info(f"get. oauth2_provider = {oauth2_provider}")

        # session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        # logger.info(f"get. session_key = {session_key}")

        # logger.info("get. set-test-key = test_value")
        request.session["test_key"] = "test_value"

        authorize_url = self.get_authorize_url(request)
        print(request.session)
        return JsonResponse({"authorize_url": authorize_url})

    def set_adapter(self):
        adapter = self.adapter_class(self.request)
        setattr(self, "adapter", adapter)

    def get_authorize_url(self, request):
        authorize_url = ""
        adapter = self.get_adapter()
        if adapter:
            provider = adapter.get_provider()
            client = self.get_client(adapter)
            action = self.request.GET.get("action", AuthAction.AUTHENTICATE)
            auth_url = adapter.authorize_url
            auth_params = provider.get_auth_params(self.request, action)

            pkce_params = provider.get_pkce_params()
            code_verifier = pkce_params.pop("code_verifier", None)
            auth_params.update(pkce_params)
            if code_verifier:
                self.request.session["pkce_code_verifier"] = code_verifier

            # logger.info(f"stash_provider provider.id= {provider.id}")
            self.stash_provider(provider.id, request)

            client.state = SocialLogin.stash_state(self.request)
            authorize_url = client.get_redirect_url(auth_url, auth_params)
        return authorize_url

    def get_adapter(self):
        return getattr(self, "adapter", None)

    def get_client(self, adapter):
        provider = adapter.get_provider()
        scope = provider.get_scope(self.request)
        client = adapter.client_class(
            self.request,
            provider.app.client_id,
            provider.app.secret,
            adapter.access_token_method,
            adapter.access_token_url,
            self.callback_url,
            scope,
            scope_delimiter=adapter.scope_delimiter,
            headers=adapter.headers,
            basic_auth=adapter.basic_auth,
        )
        return client

    def stash_provider(self, provider_name, request):
        self.request.session["oauth2_provider"] = provider_name
        session_key = self.request.COOKIES.get("sessionid")
        # logger.info(f"session_key = {session_key}")
        if session_key:
            cache_key = f"oauth2_provider_{session_key}"
            cache.set(cache_key, provider_name)

        oauth2_provider = request.session.get("oauth2_provider")
        logger.info(f"stash_provider. request = {oauth2_provider}")

        oauth2_provider = self.request.session.get("oauth2_provider")
        logger.info(f"stash_provider. self.request = {oauth2_provider}")

    def unstash_provider(self, request):
        oauth2_provider = request.session.get("oauth2_provider")
        logger.info(f"unstash_provider. request = {oauth2_provider}")

        oauth2_provider = self.request.session.get("oauth2_provider")
        logger.info(f"unstash_provider. self.request = {oauth2_provider}")

        provider = ""
        if "oauth2_provider" not in self.request.session:
            logger.error("Unable to unstash oauth2_provider from request session")

            session_key = self.request.COOKIES[settings.SESSION_COOKIE_NAME]
            # logger.info(f"session_key = {session_key}")
            if session_key:
                cache_key = f"oauth2_provider_{session_key}"
                provider = cache.get(cache_key)
                # logger.info(f"provider = {provider}")
            else:
                raise PermissionDenied()
        else:
            # provider = self.request.session.pop("oauth2_provider")
            provider = self.request.session.get("oauth2_provider")
        return provider

    @classmethod
    def get_adapter_class_by_provider_id(cls, provider_id):
        if provider_id == GitHubProvider.id:
            return GitHubOAuth2Adapter
        raise PermissionDenied()


class SignInView(OAuth2LoginView):
    http_method_names = ["post"]

    def get_response(self):
        response = super().get_response()
        data = response.data
        del data[ACCESS_TOKEN_NAME]
        del data[REFRESH_TOKEN_NAME]

        output_serializer = BaseUserResponse(self.user)
        data["user"] = output_serializer.data

        response.data = data

        return response

    def post(self, request, *args, **kwargs):
        # session_key = self.request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        # logger.info(f"post. session_key = {session_key}")

        # oauth2_provider = self.request.session.get("oauth2_provider")
        # logger.info(f"post. oauth2_provider = {oauth2_provider}")

        provider_id = self.unstash_provider(request)
        self.adapter_class = self.get_adapter_class_by_provider_id(provider_id)
        SocialLogin.verify_and_unstash_state(request, request.data.get("state"))
        return super().post(request, *args, **kwargs)


class OAuth2AuthorizeUrlView(OAuth2LoginView):
    http_method_names = ["get"]


class GithubLoginView(OAuth2AuthorizeUrlView):
    adapter_class = GitHubOAuth2Adapter


class SignOutView(LogoutView):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(REFRESH_TOKEN_NAME)
        request.data[REFRESH_TOKEN_NAME] = refresh_token
        response = super().post(request, *args, **kwargs)
        return response
