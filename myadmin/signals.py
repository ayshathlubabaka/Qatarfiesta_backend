from django.db.models.signals import ModelSignal
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail

event_request_submitted = ModelSignal()


@receiver(event_request_submitted)
def handle_event_request(sender, **kwargs):
    event_request = kwargs["event_request"]
    event_request_url = "http://localhost:3000/admin/event_request"
    event_request_url += f"/{event_request.id}"
    send_admin_notification(event_request_url=event_request_url)


def send_admin_notification(event_request_url):
    subject = "New event request"
    message = f"Click here to see submitted event request\n{event_request_url}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
