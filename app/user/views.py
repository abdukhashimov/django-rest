from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import generics

from user.serializers import UserSerializer, AuthTokenSerialier


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for a user"""
    serializer_class = AuthTokenSerialier
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
