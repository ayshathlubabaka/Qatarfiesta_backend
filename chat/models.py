from django.db import models
from accounts.models import User
from organizer.models import Events
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json


class VisitorOrganizerChat(models.Model):
    handle_user_id = models.IntegerField()
    message = models.TextField(null=True, blank=True)
    group_name = models.CharField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    from_user = models.BooleanField(default=False)

    def __str__(self):
        return self.message


class PendingChat(models.Model):
    reciever = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="organizer_chats"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="user_chats"
    )
    event = models.ForeignKey(Events, on_delete=models.CASCADE, null=True)
    chat_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pending Chat for Organizer: {self.reciever.name}"

    def save(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        count = PendingChat.objects.count()
        async_to_sync(channel_layer.group_send)(
            "count_group_name",
            {"type": "send_chatcount", "value": json.dumps({"count": (count + 1)})},
        )
        super(PendingChat, self).save(*args, **kwargs)
