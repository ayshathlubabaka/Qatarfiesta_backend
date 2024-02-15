from google.auth.transport import requests
from google.oauth2 import id_token
from accounts.models import User
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class Google:
    @staticmethod
    def validate(access_token):
        try:
            id_info = id_token.verify_oauth2_token(access_token, requests.Request())
            if "accounts.google.com" in id_info["iss"]:
                return id_info

        except Exception as e:
            return "token is invalid or has expired"


def login_social_user(email, password):
    user = authenticate(email=email, password=settings.SOCIAL_AUTH_PASSWORD)
    if user and user.is_verified:
        user_tokens = user.tokens()
        return {
            "email": user.email,
            "name": user.name,
            "access_token": str(user_tokens.get("access")),
            "refresh_token": str(user_tokens.get("refresh")),
        }
    else:
        raise AuthenticationFailed(detail="Invalid credentials or user not verified")


def register_social_user(provider, email, name):
    user = User.objects.filter(email=email)
    if user.exists():
        if provider == user[0].auth_provider:
            login_social_user(email, settings.SOCIAL_AUTH_PASSWORD)
        else:
            raise AuthenticationFailed(
                detail=f"please continue login with {user[0].auth_provider}"
            )
    else:
        new_user = {
            "email": email,
            "name": name,
            "password": settings.SOCIAL_AUTH_PASSWORD,
        }
        register_user = User.objects.create_user(**new_user)
        register_user.auth_provider = provider
        register_user.is_verified = True
        register_user.save()
        login_social_user(
            email=register_user.email, password=settings.SOCIAL_AUTH_PASSWORD
        )
