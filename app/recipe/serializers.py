from rest_framework import serializers

from core.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tag object.
    This will run first when doing any HTTP requests (POST, GET, UPDATE).
    Every input validations must be made here.
    """

    class Meta:

        """ For which model this serializer belongs to """
        model = Tag

        """
        Which fields we will accept as input or output.
        fields attribute is only available when using ModelSerializer.
        This fields will be available in the HTML form when using a browser
        and going into the url of the API.
        """
        fields = ('id', 'name')

        read_only_fields = ('id',)
