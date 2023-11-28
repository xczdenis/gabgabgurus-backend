from django.urls import path

from gabgabgurus.api.v1.notifications import views
from gabgabgurus.api.v1.notifications.consumers import UserNotifyConsumer

app_name = "notifications"

urlpatterns = [
    path("", views.NotificationListUpdateView.as_view(), name="list"),
    path("<int:pk>/", views.NotificationUpdateView.as_view(), name="update"),
]

websocket_urlpatterns = [
    path("<user_id>/", UserNotifyConsumer.as_asgi()),
]
