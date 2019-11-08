from django.test import TestCase
from django.contrib.auth import get_user_model

# docker-compose run app sh -c "python manage.py test"


class ModelTests(TestCase):
    """ All models Tests """

    def test_create_user_with_email_successful(self):
        """ Test if it can create a new user with email"""
        email = 'test@londonappdev.com'
        password = '12345678'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ Test the enail for a new user is normalized """
        email = 'test@LONDONAPPDEV.COM'
        password = '12345678'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ Test creating a user with no email raiser error """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '123')

    def test_create_new_super_user(self):
        """ test if Django creates a valid custom super user """
        email = 'test@LONDONAPPDEV.COM'
        password = '12345678'

        superuser = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
