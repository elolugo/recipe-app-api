from rest_framework import generics, authentication, permissions
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
    Rendering the HTML form for entering the email and password.
    If we exclude this line, we'll need to use a tool like curl.
    """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    RetrieveUpdateAPIView -> Used for read or update endpoints
    to represent a single model instance.
    Specific APIView for get, put, patch an object
    """

    serializer_class = UserSerializer

    """
    What permissions the user must have to access this API.
    Setting that the user must be authenticated first to acccess the API
    """
    permission_classes = (permissions.IsAuthenticated,)

    """
    How the authentication will be made eg: Cookie, session, token.
    """
    authentication_classes = (authentication.TokenAuthentication,)

    def get_object(self):
        """
        Overriding the get_object function of the APIView.
        By default, the get_object() returns a specific object using
        its primary key ID in the URL, like /profile/<id>/.
        We override this to always return the authenticated user.
        """
        return self.request.user
