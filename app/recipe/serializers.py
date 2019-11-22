from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe


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


class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ingredient object.
    This will run first when doing any HTTP requests (POST, GET, UPDATE).
    Every input validations must be made here.
    """

    class Meta:

        """ For which model this serializer belongs to """
        model = Ingredient

        """
        Which fields we will accept as input or output.
        fields attribute is only available when using ModelSerializer.
        This fields will be available in the HTML form when using a browser
        and going into the url of the API.
        """
        fields = ('id', 'name')

        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """ Serializer for the Recipe model """

    """
    How detailed the ingredient part of the GET response.
    The queryset field is used for model instance lookups
    when validating the field input of a POST method.
    To the queryset field it will be appended a .get(pk=data)
    resulting in Ingredient.objects.all().get(pk=data)
    so that it filters by primary key.
    many=True because it will be returning many instances
    Just returning the id in the DB
    """
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:

        """ For which model this serializer belongs to """
        model = Recipe

        """
        Which fields we will accept as input or output.
        fields attribute is only available when using ModelSerializer.
        This fields will be available in the HTML form when using a browser
        and going into the url of the API.
        It doesn't matter if the attribute of the model is ManyToMany
        """
        fields = (
            'id', 'title', 'ingredients', 'tags', 'time_minutes', 'price',
            'link',
        )

        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for detailed recipes"""

    """
    Nested serializer for returning the ingredients
    like it was stated in its serializer
    """
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipes"""

    class Meta:
        model = Recipe
        fields = ('id', 'image')
        read_only_fields = ('id',)
