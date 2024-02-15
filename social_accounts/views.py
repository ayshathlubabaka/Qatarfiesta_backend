from google.auth.transport import requests
from google.oauth2 import id_token
from accounts.models import User
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny


class Google:
    @staticmethod
    def validate(access_token):
        try:
            id_info = id_token.verify_oauth2_token(
                access_token, requests.Request(), clock_skew_in_seconds=10
            )
            if (
                "accounts.google.com" in id_info["iss"]
                and id_info["aud"] == settings.GOOGLE_CLIENT_ID
            ):
                return id_info
        except Exception as e:
            return None


class SocialTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data["email"] = self.user.email
        data["name"] = self.user.name
        data["refresh_token"] = str(refresh)

        return data


class SocialTokenObtainPairView(TokenObtainPairView):
    serializer_class = SocialTokenObtainPairSerializer


class GoogleSignInAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        access_token = request.data.get("access_token")
        if not access_token:
            return Response(
                {"error": "Access token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        google_user_data = Google.validate(access_token)

        if not google_user_data:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_id = google_user_data["sub"]
        except KeyError:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            "aud" not in google_user_data
            or google_user_data["aud"] != settings.GOOGLE_CLIENT_ID
        ):
            return Response(
                {"error": "Could not verify user"}, status=status.HTTP_401_UNAUTHORIZED
            )

        email = google_user_data["email"]
        name = google_user_data["name"]
        provider = "google"

        user, created = User.objects.get_or_create(
            email=email,
            defaults={"name": name, "password": settings.SOCIAL_AUTH_PASSWORD},
        )

        if created:
            user.auth_provider = provider
            user.is_registered = True
            user.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response(
            {
                "email": user.email,
                "name": user.name,
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
            status=status.HTTP_200_OK,
        )
