from django.urls import path
from .views import GoogleSignInAPIView, SocialTokenObtainPairView


urlpatterns = [
    path("google/", GoogleSignInAPIView.as_view(), name="google"),
    path("token/", SocialTokenObtainPairView.as_view(), name="token_obtain_pair"),
]
