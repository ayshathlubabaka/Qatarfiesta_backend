from django.urls import path
from .views import *


urlpatterns = [
    path("history/", VisitorOrganizerChatListAPI.as_view()),
    path("pending-chats/", ViewPendingChatsAPI.as_view()),
    path("delete-url/<int:chat_id>/", ManagePendingChatsAPI.as_view()),
    path("send-mail/", SendEmailAPIView.as_view()),
]
