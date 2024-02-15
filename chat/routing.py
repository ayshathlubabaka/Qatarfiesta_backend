from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path(
        "ws/chat/<int:current_user_id>/<int:event_id>/",
        consumers.ChatConsumer.as_asgi(),
    ),
    path("ws/chat-count/", consumers.PendingChatCountConsumer.as_asgi()),
]
