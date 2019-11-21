from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """ Base Viewset for user owned recipe attributes """

    """
    How the authentication will be made eg: Cookie, session, token.
    """
    authentication_classes = (TokenAuthentication,)

    """
    What permissions the user must have to access this API.
    Setting that the user must be authenticated first to acccess the API
    """
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        For returning objects for the current authenticated user only.
        Getter of the queryset.
        """

        """
        Filtering the queryset by the user that made the GET request
        """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """ What to do if there is a POST request """
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """
    Manage Tags in the database
    """

    """
    The queryset that should be used for returning objects from this view.
    When using GET, what would be the queryset to return as a response.
    """
    queryset = Tag.objects.all()  # Attribute of GenericAPIView

    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """ Manage ingredients in the database """

    """
    The queryset that should be used for returning objects from this view.
    When using GET, what would be the queryset to return as a response.
    """
    queryset = Ingredient.objects.all()  # Attribute of GenericAPIView

    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """ Manage recipes in the database """

    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Getter of the queryset.
        For returning objects for the current authenticated user only.
        """

        """
        Filtering the queryset by the user that made the GET request
        """
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """ Return appropraite serializer class """

        """ Checking which type of request was made eg: GET, POST, PUT... """
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """ What to do if there is a POST request """
        serializer.save(user=self.request.user)
