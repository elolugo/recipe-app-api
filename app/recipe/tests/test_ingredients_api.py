from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(TestCase):
    """ Test the publicly available ingredients API requests """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test that it return None if the user is no authenticated """

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """  Test the authorized only ingredients API requests """

    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            'test@londonappdev',
            '12345678'
        )

        self.client.force_authenticate(user=self.user)

    def test_retrieve_ingredients(self):
        """ test retrieving a list of ingredients """

        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGREDIENTS_URL)

        """
        Querying the Ingredient objects from the database
        and converting in json format to check with
        the json response of a GET.
        """
        ingredients = Ingredient.objects.all().order_by('-name')

        serialized_queryset_from_DB = IngredientSerializer(
            ingredients,
            many=True
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialized_queryset_from_DB.data)

    def test_ingredients_limited_to_user(self):
        """
        Test that only ingredients for the authenticated user are returned
        """

        user2 = get_user_model().objects.create_user(
            email='another_name@londonappdev.com',
            password='another password'
        )

        Ingredient.objects.create(user=user2, name='Kale')

        ingredient = Ingredient.objects.create(user=self.user, name='Tumeric')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        """Test creating a new ingredient"""

        payload = {'name': 'Cabbage'}

        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """Test creating invalid ingredient fails"""

        payload = {'name': ''}

        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
