from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializer import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """
    Create a new user in the system.
    Specific APIView for creating or POST an object
    """
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """ Create a new auth token for user """

    serializer_class = AuthTokenSerializer

    """
    Rendering the HTML form for entering the emal and password.
    If we exclude this line, we'll need to use a tool like curl.
    """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
