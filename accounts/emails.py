from django.core.mail import send_mail
import random
from django.conf import settings
from .models import User


def send_otp_via_email(email):
    subject = "Your account verification email"
    otp = random.randint(100000, 999999)
    message = f"Your otp is {otp}"
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])
    user_obj = User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()


def send_reset_password_email(email, reset_url, redirect_url):
    subject = "Your password reset email"
    message = (
        "Click the following link to reset your password\n"
        + reset_url
        + "?redirect_url="
        + redirect_url
    )
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email], fail_silently=False)
