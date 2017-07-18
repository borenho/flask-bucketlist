from this_app import app
from this_app.models import User, Bucketlist, BucketlistItem
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
        for k, v in self.user.users.items():
            stored_password = v['password']
            expected = {2: {'email': 'leo@email.com', 'username': 'leo', 'password': stored_password}}
            self.assertEqual(expected, result)

    def test_successful_login(self):
        """Test registered user can login successfully"""
        self.user.users = {1: {'email': 'leo@email.com', 'username': 'leo', 'password': 'pwd'}}


class BucketlistTestCase(unittest.TestCase):
    """ Test the Bucketlist class """

    def setUp(self):
        """ Setup a bucketlist """
        self.bucketlist = Bucketlist('Hiking', 'Go for hiking')

    def test_create_bucketlist_without_user_fails(self):
        """Test bucketlist creation without a new user fails"""
        User.users = {}
        result = self.bucketlist.create_bucketlist()
        expected = {1: {'user_id': 1, 'name': 'Hiking', 'description': 'Go for hiking'}}
        self.assertNotEqual(expected, result)

    def test_successful_bucketlist_creation(self):
        """Test bucketlist creation is successful"""
        self.bucketlist.bucketlists = {}
        result = self.bucketlist.create_bucketlist()
        expected = {2: {'user_id': 2, 'name': 'Hiking', 'description': 'Go for hiking'}}
        self.assertEqual(expected, result)
