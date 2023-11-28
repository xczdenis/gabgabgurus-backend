from django.urls import path

from gabgabgurus.api.v1.auth.views import CookieTokenRefreshView, SignInView, SignupView

app_name = "auth"

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("token/refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
]
