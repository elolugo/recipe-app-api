from rest_framework.decorators import action  # For adding actions to ViewSet
from rest_framework.response import Response  # For returning a custom response
from rest_framework import viewsets, mixins, status
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
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """ What to do if there is a POST request """
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """
        Uploading an image to a recipe
        through 127.0.0.1:8000/api/recipes/recipe/{id}/upload-image
        """

        """Retrieving the object based in the id in the URL"""
        recipe = self.get_object()

        """
        Using get_serializer as best practice
        instead of using the RecipeImageSerializer directly.
        """
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
