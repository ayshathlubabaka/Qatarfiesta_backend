from django.db.models.signals import Signal
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import User

websocket_connected = Signal()


@receiver(websocket_connected)
def user_connected_handler(sender, **kwargs):
    user_id = kwargs.get("user_id")
    user = User.objects.get(id=user_id)
    event_id = kwargs.get("event_id")
    organizer_id = kwargs.get("organizer_id")
    chat_url = f"http://localhost:3000/organizer/chat/{user_id}/{event_id}"

    send_notification_email(chat_url=chat_url, organizer_id=organizer_id)


def send_notification_email(chat_url, organizer_id):
    subject = "User Connected to WebSocket"
    message = f"Click here to start chat \n{chat_url}"
    from_email = settings.EMAIL_HOST_USER
    organizer = User.objects.get(id=organizer_id)
    recipient_list = [organizer.email]

    send_mail(subject, message, from_email, recipient_list)
