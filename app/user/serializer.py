from django.contrib.auth import get_user_model, authenticate
""" Using a translation text file when outputting messages to the user """
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the users object.
    This will run first when doing any HTTP requests (POST, GET, UPDATE).
    Every input validations muste be made here.
    """

    class Meta:

        """ For which model this serializer belongs to """
        model = get_user_model()

        """
        Which fields we will accept as input or output.
        fields variable only available when using ModelSerializer.
        This fields will be available in the HTML form when using a browser
        and going into the url of the API.
        """
        fields = ('email', 'password', 'name')

        """ Input validations """
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }

    def create(self, validated_data):
        """ Create a new user with encypted password and return it """
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """ Serializer for the user authentication object"""

    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False  # Is possible to have a password with whitespace
    )

    def validate(self, attrs):
        """
        Validate and authenticate the user.
        attrs variable are all the fields in the serializer.
        """

        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),  #
            username=email,
            password=password
        )

        if not user:
            msg = _(' Unable to authenticate with provided credentials ')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user

        return attrs  # Must return attrs in validate()
