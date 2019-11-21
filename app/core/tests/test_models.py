from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


# docker-compose run app sh -c "python manage.py test"
def sample_user(email='test@londonappdev.com', password='testpass'):
    """ Helper function for creating a sample user """
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        """ Test the tag string representation """
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """
        Test that Ingredient created successfuly
        by requesting its string representation
        """

        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """
        Test that Recipe created successfuly
        by requesting its string representation
        """

        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    # mocking the behaviour of the function that returns the id
    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """
        Test that the image uploaded for a recipe
        is saved in the correct location
        """

        uuid = 'test-uuid'

        """
        Everytime uuid.uuid4 is called within our test,
        it will return what's inside of uuid.
        """
        mock_uuid.return_value = uuid

        """
        Generating and returning the file path of where the image will save
        """
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'

        self.assertEqual(file_path, exp_path)
