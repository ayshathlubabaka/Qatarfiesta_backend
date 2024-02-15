from rest_framework import serializers

class GoogleSignInSerializer(serializers.Serializer):
    access_token = serializers.CharField(min_length=6)
        