from rest_framework import serializers
from .models import VisitorOrganizerChat, PendingChat


class VisitorOrganizerChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorOrganizerChat
        fields = "__all__"


class PendingChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingChat
        fields = "__all__"
