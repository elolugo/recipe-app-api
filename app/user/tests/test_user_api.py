from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status  # Human readable status codes for responses
""" Client for making API requests. Getting the response of an API request """
from rest_framework.test import APIClient


""" Constants or helper functions """

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """ Helper function for creating user for every Test """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """ Test the users API for unathenticated requests (public) """

    def setUp(self):
        """ Setting the client (response) for every test """
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """
        Test creating user through a POST method
        to the API with a valid payload.
        """

        """
        Preparing the data that will be sent through
        a POST to the API
        """
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
            'name': 'Test name'
        }

        """ Makesa HTTP POST request to CREATE_USER_URL """
        res = self.client.post(CREATE_USER_URL, payload)

        """ We expect a 'created' (201) response"""
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        """ Test that the user actually exists in the database """
        user = get_user_model().objects.get(**res.data)

        self.assertTrue(user.check_password(payload['password']))

        """
        Making sure that the password
        is not in the object created response
        """
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """ Test creating a user that already exists and fails """

        payload = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
            'name': 'Test name'
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ Tests that the password must be more than 5 characters """

        payload = {
            'email': 'test@londonappdev.com',
            'password': 'pw'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        """ Check that the user is never created """
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """
        Test that token is created for a user
        that provides valid credentials
        """

        payload = {
            'email': 'test@londonappdev.com',
            'password': 'testpass'
        }

        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        """ Check that there is a token in the post response """
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """
        Test that the token does not create when
        invalid credentials are given
        """

        create_user(email='test@londonappdev.com', password="testpass")

        payload = {
            'email': 'test@londonappdev.com',
            'password': 'wrongpass'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_without_user_existing(self):
        """ Test that token is not created if user doesn't exist """

        payload = {
            'email': 'test@londonappdev.com',
            'password': 'wrongpass'
        }

        """ User is not created before making the POST """
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        """
        Test that token is not created
        if the email or password is not given
        """

        """ Blank email """
        payload = {
            'email': '',
            'password': 'wrongpass'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        """ Blank password """
        payload = {
            'email': 'test@londonappdev.com',
            'password': ''
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
