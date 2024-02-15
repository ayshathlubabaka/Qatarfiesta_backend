from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.core.mail import send_mail

from .models import VisitorOrganizerChat, PendingChat
from .serializer import VisitorOrganizerChatSerializer, PendingChatsSerializer


class IsOrganizerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if (
            request.user.is_active
            and request.user.is_organizer
            and request.user.is_registered
        ):
            return request.user.is_organizer

        return False


class VisitorOrganizerChatListAPI(generics.ListAPIView):
    model = VisitorOrganizerChat
    serializer_class = VisitorOrganizerChatSerializer

    def get_queryset(self):

        group_name = self.request.query_params.get("group_name")

        if group_name is not None:
            return VisitorOrganizerChat.objects.filter(group_name=group_name).order_by(
                "-timestamp"
            )
        else:
            return VisitorOrganizerChat.objects.none()

    def get_paginated_response(self, data):
        return Response(
            {
                "next": (
                    self.paginator.page.number + 1
                    if self.paginator.page.has_next()
                    else None
                ),
                "previous": (
                    self.paginator.page.number - 1
                    if self.paginator.page.number > 1
                    else None
                ),
                "count": self.paginator.page.paginator.count,
                "results": data,
            }
        )


class ViewPendingChatsAPI(APIView):
    def get(self, request):
        organizer = request.user
        pendingchats = PendingChat.objects.filter(reciever=organizer)
        serializer = PendingChatsSerializer(pendingchats, many=True)
        data = serializer.data
        return Response(data)


class ManagePendingChatsAPI(APIView):
    def delete(self, request, chat_id):
        try:
            pendingchat = PendingChat.objects.get(id=chat_id)
            chat_url = pendingchat.chat_url
            chats = PendingChat.objects.filter(chat_url=chat_url)
            chats.delete()
            return Response(status=status.HTTP_200_OK)
        except PendingChat.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SendEmailAPIView(APIView):
    def post(self, request, *args, **kwargs):
        sender = request.user
        sender_email = sender.email
        recipient = request.data.get("recipient")
        subject = request.data.get("subject")
        message = request.data.get("message")

        try:
            send_mail(
                subject,
                message,
                sender_email,
                [recipient],
                fail_silently=False,
            )
            return Response(
                {"message": "Email sent successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": "Failed to send email"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
