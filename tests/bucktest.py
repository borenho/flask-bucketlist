from this_app import app
from this_app.models import User
import unittest


class BasicTestCase(unittest.TestCase):
    """ Basic flask setup tests """

    def test_index(self):
        """ Initial test to ensure flask was setup correctly """
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)


class UserTestCase(unittest.TestCase):
    """ Test the User class """

    def setUp(self):
        """ Setup a new user """
        self.user = User('leo@email.com', 'leo', 'pwd')

    def test_successful_signup(self):
        """Test new user can sign up successfully"""
        self.user.users = {}
        result = self.user.create_user()
        expected = {1: {'email': 'leo@email.com', 'username': 'leo', 'password': 'pwd'}}
        self.assertEqual(expected, result)

    def test_successful_login(self):
        """Test registered user canlogin successfully"""
        self.user.users = {1: {'email': 'leo@email.com', 'username': 'leo', 'password': 'pwd'}}