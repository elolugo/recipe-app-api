import tempfile
import os

from PIL import Image  # PIL is the Pillow requirement

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


RECIPE_URL = reverse('recipe:recipe-list')


def image_upload_url(recipe_id):
    """ Return URL fro recipe image upload """
    return reverse('recipe:recipe-upload-image', args=[recipe_id])


def detail_url(recipe_id):
    """ Return recipe detail URL """
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_tag(user, name='Main course'):
    """ Helper function for creating tags """

    return Tag.objects.create(
        user=user,
        name=name
    )


def sample_ingredient(user, name='Cinnamon'):
    """ Helper function for creating ingredients """

    return Ingredient.objects.create(
        user=user,
        name=name
    )


def sample_recipe(user, **params):
    """ Helper function for creating recipes """

    """ for not writing every single time this fields """
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': 5.00
    }

    """
    Override any field of the defaults dictionary.
    Updating the keys:field from params to defaults
    if params has any similar key.
    If params has a new key, then it appends to defaults.
    """
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTests(TestCase):
    """ Test the publicly available Recipe API requests """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ Test that it return None if the user is not authenticated """

        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """  Test the authorized only Recipe API requests """

    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            'test@londonappdev',
            '12345678'
        )

        self.client.force_authenticate(user=self.user)

    def test_retrieve_recipes(self):
        """ test retrieving a list of recipes """

        sample_recipe(self.user, title='Soyo')
        sample_recipe(self.user, title='Tortilla')

        res = self.client.get(RECIPE_URL)

        """
        Querying the Recipe objects from the database
        and converting in json format to check with
        the json response of a GET.
        """
        recipes = Recipe.objects.all().order_by('-id')

        serialized_queryset_from_DB = RecipeSerializer(
            recipes,
            many=True
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialized_queryset_from_DB.data)

    def test_ingredients_limited_to_user(self):
        """
        Test that only recipes for the authenticated user are returned
        """

        user2 = get_user_model().objects.create_user(
            email='another_name@londonappdev.com',
            password='another password'
        )

        sample_recipe(user2, title='Soyo')

        user_recipe = sample_recipe(self.user, title='Tortilla')

        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], user_recipe.title)

    def test_view_recipe_detail(self):
        """ Test viewing in detail any recipe by its URL """

        recipe = sample_recipe(user=self.user)

        """ Adding a tag and an ingredient to the recipe object """
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        """
        Generating the url for this specific recipe.
        """
        url = detail_url(recipe.id)  # api/recipes//recipe/{id}

        res = self.client.get(url)

        """
        Serializing the recipe object into a json
        """
        serialized_recipe = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serialized_recipe.data)

    def test_create_basic_recipe(self):
        """ Test creating recipe """

        payload = {
            'title': 'Chocolate Cheesecake',
            'time_minutes': 30,
            'price': 5.00
        }

        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])

        """
        looping through the keys of the recipe retrieved from te DB
        and checking of its the same as the payload sent
        """
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags(self):
        """ test creating a recipe with tags """

        tag1 = sample_tag(user=self.user, name='Vegan')
        tag2 = sample_tag(user=self.user, name='Dessert')

        """ Sending several ids in a POST request """
        payload = {
            'title': 'Avocado lime cheescake',
            'tags': [tag1.id, tag2.id],
            'time_minutes': 60,
            'price': 20.00
        }

        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        """ Getting the tags associated with the recipe POSTed"""
        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()

        """ Checking that 2 tags got associated with the new recipe """
        self.assertEqual(tags.count(), 2)

        """
        Check that the tags object created for the POST
        are the same as the one POSTed.
        assertIn che
        """
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_recipe_with_ingredients(self):
        """ Test create a recipe with ingredients """

        ingredient1 = sample_ingredient(user=self.user, name='Prawns')
        ingredient2 = sample_ingredient(user=self.user, name='Ginger')

        payload = {
            'title': 'Thai prawn red curry',
            'ingredients': [ingredient1.id, ingredient2.id],
            'time_minutes': 20,
            'price': 7.00
        }

        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])

        """ Returns a list of Ingredient objects """
        ingredients = recipe.ingredients.all()

        self.assertEqual(ingredients.count(), 2)

        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)

    def test_partial_update_recipe(self):
        """ Test updating a recipe with a PATCH """

        recipe = sample_recipe(user=self.user)

        recipe.tags.add(sample_tag(user=self.user))

        new_tag = sample_tag(user=self.user, name='Curry')

        payload = {
            'title': 'Chicken tikka',
            'tags': [new_tag.id]
        }

        url = detail_url(recipe.id)

        self.client.patch(url, payload)

        """
        Updating the recipe variable with what's in the DB
        """
        recipe.refresh_from_db()

        self.assertEqual(recipe.title, payload['title'])

        """ Returns a list of Tag objects """
        tags = recipe.tags.all()

        self.assertEqual(tags.count(), 1)

        self.assertIn(new_tag, tags)

    def test_full_update_recipe(self):
        """ Testing a PUT request for a recipe """

        recipe = sample_recipe(user=self.user)

        recipe.tags.add(sample_tag(user=self.user))

        """
        The object will be replaced with this payload when doing a PUT
        """
        payload = {
            'title': 'Spaghetti Carbonara',
            'time_minutes': 25,
            'price': 5.00
        }

        url = detail_url(recipe.id)
        self.client.put(url, payload)

        """
        Updating the recipe variable with what's in the DB
        """
        recipe.refresh_from_db()

        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.time_minutes, payload['time_minutes'])
        self.assertEqual(recipe.price, payload['price'])

        """
        Checking that since the payload didn't contain any tags,
        the tags field from the recipe were removed
        """
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 0)


class RecipeImageUploadTests(TestCase):
    """  """
    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            'test@londonappdev',
            '12345678'
        )

        self.client.force_authenticate(user=self.user)

        self.recipe = sample_recipe(self.user)

    def tearDown(self):
        """Opposite of setUp, running after all the tests"""

        """Deleting the created image for cleaning the files created"""
        self.recipe.image.delete()

    def test_upload_image(self):
        """Testing that an image uploaded successfully"""

        url = image_upload_url(self.recipe.id)

        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            """Creating a temporary file in the system with .jpg extension"""

            img = Image.new('RGB', (10, 10))  # Creating a random image 10x10
            img.save(ntf, format='JPEG')  # Saving into a JPEG format
            ntf.seek(0)  # Reverting back the pointer into the first byte

            """
            Sending an image into a POST request.
            The multipart option is for changin the default json format,
            from json to multipart for sending data.
            """
            res = self.client.post(url, {'image': ntf}, format='multipart')

            self.recipe.refresh_from_db()

            self.assertEqual(res.status_code, status.HTTP_200_OK)

            self.assertIn('image', res.data)

            """ Checking if the image exists in the back-end system """
            self.assertTrue(os.path.exists(self.recipe.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url(self.recipe.id)

        """Expecting an ImageFile object but sending a string"""
        res = self.client.post(url, {'image': 'notimage'}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
