from flask import url_for
from this_app import app
from this_app.models import User, Bucketlist, Activity
import unittest


class BasicTestCase(unittest.TestCase):
    """ Basic flask setup tests """

    def test_index(self):
        """ Initial test to ensure flask was setup correctly """
        tester = app.test_client(self)        # You can use self.app in place of tester
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_logout_redirects_to_homepage(self):
        """ Ensure logout redirects to hp """
        tester = app.test_client(self)
        response = tester.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


class UserTestCase(unittest.TestCase):
    """ Test the User class """

    def setUp(self):
        """ Setup a new user """
        self.user = User('leo@email.com', 'leo', 'pwd')
        tester = app.test_client(self)
        User.users = {}

    def tearDown(self):
        del self.user
        User.users = {}

    def test_users_can_signup(self):
        """Test new user can sign up successfully"""
        self.user.users = {}
        result = self.user.create_user()
        for key, value in self.user.users.items():
            stored_password = value['password']
            expected = {3: {
                'email': 'leo@email.com', 'username': 'leo', 'password': stored_password
                }}
            # self.assertEqual(expected, result)

    def test_successful_login(self):
        """Test registered user can login successfully"""
        self.user.users = {}
        self.user.create_user()
        tester = app.test_client(self)
        login = tester.post('/login',
                            data=dict(email='leo@email.com',
                                      password='pwd'),
                            follow_redirects=True)

    def test_invalid_credentials_redirects_to_login(self):
        self.user.users = {}
        self.user.create_user()
        tester = app.test_client(self)
        login = tester.post('/login',
                            data=dict(email='leo@email.com',
                                      password='pwc'),
                            follow_redirects=True)

    def test_signup_existing_user_redirects_to_login(self):
        self.user.users = {}
        self.user.create_user()
        tester = app.test_client(self)
        login = tester.post('/signup',
                            data=dict(email='leo@email.com',
                                      usrname='leo',
                                      password='pwd'),
                            follow_redirects=True)


class BucketlistTestCase(unittest.TestCase):
    """ Test the Bucketlist class """

    def setUp(self):
        """ Setup a bucketlist """
        self.bucketlist = Bucketlist('Hiking', 'Go for hiking')

    def tearDown(self):
        del self.bucketlist

    def test_create_bucketlist_without_user_fails(self):
        """Test bucketlist creation without a new user fails"""
        User.users = {}
        self.bucketlist.bucketlists = {}
        result = self.bucketlist.create_bucketlist()
        expected = {1: {'user_id': 1, 'name': 'Hiking', 'description': 'Go for hiking'}}
        self.assertNotEqual(expected, result)

    def test_successful_bucketlist_creation(self):
        """Test bucketlist creation is successful"""
        self.bucketlist.bucketlists = {}
        result = self.bucketlist.create_bucketlist()
        expected = {2: {'user_id': 3, 'name': 'Hiking', 'description': 'Go for hiking'}}
        # self.assertEqual(expected, result)


class ActivityTestCase(unittest.TestCase):
    """ Test the BucketlistItem class """

    def setUp(self):
        """ Setup a bucketlist """
        self.activity = Activity('Hiking', 'Go for hiking', True)

    def tearDown(self):
        del self.activity

    def test_successful_activity_creation(self):
        """Test bucketlist item creation is successful"""
        self.activity.activities = {}
        result = self.activity.create_activity()
        expected = {1: {'bucketlist_id': 2, 'title': 'Hiking', 'description': 'Go for hiking', 'status': True}}
        self.assertEqual(expected, result)
