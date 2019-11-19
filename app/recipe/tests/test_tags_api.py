from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

"""
The serializer of the recipe model
for converting into json the Tags objects saved in the database
"""
from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')  # ?????


class PublicTagsApiTests(TestCase):
    """ Test the public available tags API. """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test that it cannot list the tags without authentication. """

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """ Test the authenticated API methods. """

    def setUp(self):

        self.user = get_user_model().objects.create_user(
            email='test@londonappdev.com',
            password='12345678',
            name='test name'
        )

        self.client = APIClient()

        """ authenticating the created user for the tests. """
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tags(self):
        """ Test a GET for retrieving for tags. """

        Tag.objects.create(name='Vegan', user=self.user)
        Tag.objects.create(name='Dessert', user=self.user)

        res = self.client.get(TAGS_URL)

        """
        Querying the Tags objects from the database
        and converting in json format to check with
        the json response of a GET.
        """
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        """
        Checking if the GET result json is the same that the one serialized.
        """
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """
        Test that all the tags retrieved from the DB
        are from the user that made the GET request.
        """

        user2 = get_user_model().objects.create_user(
            email='another_test_user@londonappdev.com',
            password='87654321'
        )

        Tag.objects.create(name='Fruity', user=user2)
        tag = Tag.objects.create(name='Comfort Food', user=self.user)

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        """ Checking that it only returned 1 item in the GET response. """
        self.assertEqual(len(res.data), 1)

        """
        Checking that the name of the tag returned
        is the same that the tag created for the user.
        """
        self.assertEqual(res.data[0]['name'], tag.name)
