from django.urls import path

from gabgabgurus.api.v1.chats import views
from gabgabgurus.api.v1.chats.consumers import ChatConsumer

app_name = "chats"

urlpatterns = [
    path("channels/", views.ChannelListCreateView.as_view()),
    path("user-channels/", views.UserChannelListCreateView.as_view()),
    path("user-channels/<int:channel_id>/messages/", views.MessageListCreateView.as_view()),
]

websocket_urlpatterns = [
    path("<chat_id>/", ChatConsumer.as_asgi()),
]
