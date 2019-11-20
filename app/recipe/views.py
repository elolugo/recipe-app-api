from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient

from recipe import serializers


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """
    Manage Tags in the database
    """

    """
    What permissions the user must have to access this API.
    Setting that the user must be authenticated first to acccess the API
    """
    permission_classes = (IsAuthenticated,)

    """
    How the authentication will be made eg: Cookie, session, token.
    """
    authentication_classes = (TokenAuthentication,)

    """
    The queryset that should be used for returning objects from this view.
    When using GET, what would be the queryset to return as a response.
    """
    queryset = Tag.objects.all()

    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """ Return objects for the current authenticated user only """

        """
        Filtering the queryset before responding the GET request
        """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """ Runs everytime a new POST request is made """
        serializer.save(user=self.request.user)


class IngredientViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    """ Manage ingredients in the database """

    """
    What permissions the user must have to access this API.
    Setting that the user must be authenticated first to acccess the API
    """
    permission_classes = (IsAuthenticated,)

    """
    How the authentication will be made eg: Cookie, session, token.
    """
    authentication_classes = (TokenAuthentication,)

    """
    The queryset that should be used for returning objects from this view.
    When using GET, what would be the queryset to return as a response.
    """
    queryset = Ingredient.objects.all()  # Attribute of GenericAPIView

    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        """
        For returning objects for the current authenticated user only.
        Getter of the queryset.
        """

        """
        Filtering the queryset before responding the GET request
        """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """ What to do if there is a POST request """
        serializer.save(user=self.request.user)
