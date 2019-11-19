from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag

from recipe import serializers


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
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

    queryset = Tag.objects.all()

    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """ Return objects for the current authenticated user only """

        """
        Filtering the queryset before responding the GET request
        """
        return self.queryset.filter(user=self.request.user).order_by('-name')
