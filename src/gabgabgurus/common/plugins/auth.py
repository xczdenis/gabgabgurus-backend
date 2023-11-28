from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """
    An authentication plugin that authenticates requests through a JSON web
    token provided in a http only cookie.
    """

    def authenticate(self, request):
        raw_token = self.get_raw_token_from_cookie(request)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token

    def get_raw_token_from_cookie(self, request):
        return request.COOKIES.get("access")
