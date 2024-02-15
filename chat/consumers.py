from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import VisitorOrganizerChat, PendingChat
from channels.db import database_sync_to_async
from organizer.models import Events
from .signals import websocket_connected
from accounts.models import User
from asgiref.sync import async_to_sync
import json


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        current_user_id = self.scope["url_route"]["kwargs"]["current_user_id"]
        event_id = self.scope["url_route"]["kwargs"]["event_id"]

        self.room_name = f"{current_user_id}-{event_id}"

        self.room_group_name = "chat_%s" % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data["message"]
        current_user_id = data["current_user_id"]
        from_user = data["from_user"]

        await self.save_message(
            handle_user_id=current_user_id,
            message=message,
            from_user=from_user,
            group_name=self.room_group_name,
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "current_user_id": current_user_id,
                "from_user": from_user,
            },
        )

        event_id = self.scope["url_route"]["kwargs"]["event_id"]
        organizer_id = await self.get_organizer_id(event_id)
        await self.send_mail(current_user_id, event_id, organizer_id)
        await self.create_pending_chat(current_user_id, event_id, organizer_id)

    async def disconnect(self, code):
        self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def chat_message(self, event):
        message = event["message"]
        current_user_id = event["current_user_id"]
        from_user = event["from_user"]
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "current_user_id": current_user_id,
                    "from_user": from_user,
                }
            )
        )

    async def send_pending_chat_update(self, event):
        pending_chat_count = event["pending_chat_count"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "pending_chat_update",
                    "pending_chat_count": pending_chat_count,
                }
            )
        )

    @database_sync_to_async
    def save_message(self, handle_user_id, message, from_user, group_name):
        VisitorOrganizerChat.objects.create(
            handle_user_id=handle_user_id,
            message=message,
            group_name=group_name,
            from_user=from_user,
        )

    @database_sync_to_async
    def get_organizer_id(self, event_id):
        try:
            event = Events.objects.get(id=event_id)
            return event.organizer.id
        except Events.DoesNotExist:
            return None

    @database_sync_to_async
    def send_mail(self, current_user_id, event_id, organizer_id):
        websocket_connected.send(
            sender=self.__class__,
            user_id=current_user_id,
            event_id=event_id,
            organizer_id=organizer_id,
        )

    @database_sync_to_async
    def create_pending_chat(self, current_user_id, event_id, organizer_id):
        user = User.objects.get(id=current_user_id)
        event = Events.objects.get(id=event_id)
        organizer = User.objects.get(id=organizer_id)
        chat_url = f"http://localhost:3000/organizer/chat/{current_user_id}/{event_id}"
        PendingChat.objects.create(
            reciever=organizer, chat_url=chat_url, user=user, event=event
        )


class PendingChatCountConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "count_group_name"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        self.send(text_data="group created")

    async def receive(self, text_data=None, bytes_data=None):
        self.send(text_data="This is from server")

    async def disconnect(self, close_code):
        self.close(close_code)

    async def send_chatcount(self, event):
        await self.send(text_data=event["value"])
