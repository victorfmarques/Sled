from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.serializers import api_settings

from . import serializers


class CreateUserView(generics.CreateAPIView):
    """ Creates an user"""
    serializer_class = serializers.UserSerializer


class CreateTokenView(ObtainAuthToken):
    """ Creates user auth token """
    serializer_class = serializers.TokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
