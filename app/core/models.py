import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings


def recipe_image_file_path(instance, filename):
    """
    Function that generates a random filename
    for the images uploaded
    """

    """
    Spliting the filename into 2 parts by the . and returning
    the last part (extension eg: jpg, png)
    """
    ext = filename.split('.')[-1]

    """ Generating a random filename and appending the extension """
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/recipe/', filename)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Replacing the default create_user function.
        Custom function for creating a new user model, either by
        command line or though code
        """

        """
        raises an error if the email is not provided when creating a new user
        """
        if not email:
            raise ValueError('User must have an email address')

        """
        (XXXX@YYY.com) lowercase the mail portion -> YYYY
        """
        email = self.normalize_email(email)

        """
        Create a new UserProfile object and sets the email.
        We can access the model that the manager is for by self.model
        It's the same as creating a new user model and assigning to the user
        variable
        """
        user = self.model(email=email, **extra_fields)

        """
        If we set the password when creating a model, it will be stored as a
        plain text. It's important to hash the password and then save it
        """
        user.set_password(password)

        """
        Saving the new user in the database
        """
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        create new super user profile.
        What Django will do when creating a new super user through
        the command line or through code
        """

        """
        creates a new 'normal' user with the mail and name provided
        """
        user = self.create_user(email, password)

        """
        Set the status of super user as true.
        Set the status of staff member as true.
        """
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)  # saving the new super user in the database

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports using email instead of username.
    Custom user model for storing in the database.
    """

    """
    The email field. Every email in the system must be unique
    """
    email = models.EmailField(max_length=255, unique=True)

    """
    All the other fields/columns in the database
    """
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)  # default value is true
    is_staff = models.BooleanField(default=False)

    """
    Setting the custom UserManager for this user model.
    """
    objects = UserManager()

    """
    Setting and overwritting the standard Django username to the email field
    """
    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """ Tag to be used for a recipe """
    name = models.CharField(max_length=255)

    """
    Assigning the User model the recommended way.
    From the settings if we change the name of the class of the user
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """ Ingredient to be used in a recipe """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """ Recipe """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    """
    Passing the class as a string because if we pass the class directly,
    the class has to be in the same order that you use it.
    First -> Ingredients
    Second -> Tag
    When passing the class name as a string it doesn't matter the order.
    """
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')

    """ Just referencing the function and not calling it """
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title
