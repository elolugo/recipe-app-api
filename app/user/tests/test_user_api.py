from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status  # Human readable status codes for responses
""" Client for making API requests. Getting the response of an API request """
from rest_framework.test import APIClient


""" Constants or helper functions """

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')  # The URL of a user -> user/{id_user}


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

    def test_retrieve_user_unauthorized(self):
        """
        Test that an unauthorized user cant retrieve any users data.
        Test that authentication is required for users API.
        """

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """ Test the users API for athenticated requests (with a token) """

    def setUp(self):
        """ Creating a user and authenticate it """
        self.user = create_user(
            email='test@londonappdev.com',
            password='test_password',
            name='testName'
        )

        self.client = APIClient()

        """ authenticating the created user for the tests """
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """ Test retrieving profile for logged in user """

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            # Referencing the user created in the setup
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """ Test that a user can't POST on his own profile """

        """ POST just an empty object """
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """ Test updating the user profile for authenticated user """

        payload = {
            'email': 'newmail@londonappdev.com',
            'name': 'newname',
            'password': 'newpassword'
        }

        res = self.client.patch(ME_URL, payload)

        """ Updating the setUp user object with what's in the DB """
        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
