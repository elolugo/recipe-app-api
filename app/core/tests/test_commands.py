# Importing patch for mocking tests
from unittest.mock import patch
# TODO Importing call_command for calling   asdadasfaf
from django.core.management import call_command
# The error when postgresql database is not ready yet
from django.db.utils import OperationalError
from django.test import TestCase


class commandTests(TestCase):
    """ Testing the commands when using the database """
    def test_wait_for_db_ready(self):
        """
        Mocking an up Database.
        Testing the function that is in charge for checking
        if the database is ready before using it.
        """

        """
        Overwriting the Connection handler so that it always returns true
        instead of an exception(OperationalError).
        The __getitem___ function is called whenever retrieving
        the database is required
        """
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # Setting the return value of getting the database object to true
            gi.return_value = True
            # Calling the management command 'wait_for_db'
            call_command('wait_for_db')
            # Asserting that gi function was called once
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)  # 'time.sleep'funcion->True always
    def test_wait_for_db(self, ts):  # 2nd argument is the one passed on @patch
        """
        Test waiting for the DB to be up.
        Checking if the function 'wait_for_db' is called 5 times
        if the database is down. On the 6th try it will be up
        """

        """
        Overwriting the Connection handler so that it always returns true
        instead of an exception(OperationalError).
        The __getitem___ function is called whenever retrieving
        the database is required
        """
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:

            """
            Raising OperationalError 5 times and the returning True
            """
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
