from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    """ All Admin page Tests """
    def setUp(self):
        """ A set up function that runs before every test in this class """

        """
        A helper function that emulates a browser.
        It's a class that emulates the behaivour of a browser like GET and POST
        """
        self.client = Client()

        """
        Creating a superuser that will work as a dummy superuser
        and storing in an attribute of this class called 'admin_user'
        """
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@londonappdev.com',
            password='password123'
        )

        """
        Method to simulate the effect of a user logging into the site.
        """
        self.client.force_login(self.admin_user)

        """
        Creating a regular user that will work as a dummy user
        and storing in an attribute of this class called 'user'
        """
        self.user = get_user_model().objects.create_user(
            email='test@londonappdev.com',
            password='password123',
            name='test user full name'
        )

    def test_users_listed(self):
        """
        Test if the Django admin site supports our custom User model.
        Test if lists all the Users with the correct fields.
        Email instead of username
        """

        """
        Retrieving the url for the 'list users page'
        """
        url = reverse('admin:core_user_changelist')

        """
        GET the 'list users page'. Getting all the users in a json format
        """
        res = self.client.get(url)

        """
        Check if the regular user is contained in the GET response
        of the 'list users page'
        """
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """ Test that the user edit page works """
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/1
        res = self.client.get(url)

        """
        Checking if the page got rendered correctly
        """
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """ Test that the create user page works """
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
