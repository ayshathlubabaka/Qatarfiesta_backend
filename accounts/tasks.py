from celery import shared_task
from qatarfiesta.celery import app
from .models import User
from django.core.mail import send_mail
from qatarfiesta import settings
from django.utils import timezone
import datetime


@app.task(name="send_notification", bind=True)
def send_notification(self):
    try:
        time_threshold = timezone.now() - datetime.timedelta(hours=2)
        user_objs = User.objects.filter(
            is_registered=False, date_joined__gte=time_threshold
        )
        print("Users to Notify:", user_objs)
        for user_obj in user_objs:
            subject = "Your Qatarfiesta account is not verified"
            message = "Your account is not verified. Enter the previously sent otp to verify your account"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user_obj.email]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)
        return "Done"

    except Exception as e:
        print(e)
