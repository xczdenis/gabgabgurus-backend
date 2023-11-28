from gabgabgurus.apps.users.services import set_user_last_activity_in_cache


class PresenceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.set_user_online(request)
        return response

    def set_user_online(self, request):
        request_user = getattr(request, "user", None)
        if request_user is not None:
            if getattr(request_user, "is_authenticated", False):
                set_user_last_activity_in_cache(request_user.id)
