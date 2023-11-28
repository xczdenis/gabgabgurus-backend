from django.urls import path

from gabgabgurus.api.v1.oauth.views import GithubLoginView, SignInView, SignOutView

app_name = "oauth"

urlpatterns = [
    path("signin/", SignInView.as_view(), name="sign_in"),
    path("signout/", SignOutView.as_view(), name="sign_out"),
    path("github/", GithubLoginView.as_view(), name="github_login"),
]
