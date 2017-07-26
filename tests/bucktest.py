from flask import url_for, session
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
        User.users = {}
        self.app = User('leo@email.com', 'leo', 'pwd')
        # Initialize the test client
        self.client = app.test_client(self)
        # Set some default user data
        self.user_data = {
            1 : {'leo@email.com', 'leo', 'pwd'},
            2 : {'trieu@email.com', 'trieu', 'pwwd'}
        }

    def test_users_can_signup(self):
        """Test new user can sign up successfully"""
        for key, value in self.app.users.items():
            result = self.app.create_user()
            stored_password = value['password']
            expected = {0: {
                'email': 'leo@email.com', 'username': 'leo', 'password': stored_password
                }}
            self.assertEqual(expected, result)

    def test_successful_login(self):
        """Test registered user can login successfully"""
        tester = app.test_client(self)
        response = tester.post('/login',
                            data=dict(email='leo@email.com',
                                      password='pwd'),
                            follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_invalid_credentials_redirects_to_login(self):
        """Users need valid credentials"""
        tester = app.test_client(self)
        response = tester.post('/login',
                            data=dict(email='leo@email.com',
                                      password='pwc'),
                            follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_signup_existing_user_redirects_to_login(self):
        """Users get redirected to login if they have a/c"""
        tester = app.test_client(self)
        response = tester.post('/signup',
                            data=dict(email='leo@email.com',
                                      usrname='leo',
                                      password='pwd'),
                            follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_show_bucketlists_without_login_redirects(self):
        """Users need valid credentials"""
        tester = app.test_client(self)
        response = tester.post('/show_bucketlists', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_bucketlists_dashboard_without_login_redirects(self):
        """Users need valid credentials"""
        tester = app.test_client(self)
        response = tester.get('/show_bucketlists', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        del self.app
        del self.user_data


class BucketlistTestCase(unittest.TestCase):
    """ Test the Bucketlist class """

    def setUp(self):
        """ Setup a bucketlist """
        User.users = {1: {'leo@email.com', 'leo', 'pwd'}}
        self.bucketlist = Bucketlist('Hiking', 'Go for hiking')

    def tearDown(self):
        del self.bucketlist 
        del User.users
    
    # def test_update_bucketlist(self):
    #     """ Users can update bucketlists """
    #     self.bucketlist.bucketlists = {}
    #     self.bucketlist.create_bucketlist()
    #     former = self.bucketlist
    #     self.bucketlist.edit_bucketlist()
    #     latter = self.bucketlist
    #     self.assertNotEqual(former, latter)

    def test_create_bucketlist_without_user_fails(self):
        """Test bucketlist creation without a user fails"""
        User.users = {}
        result = self.bucketlist.create_bucketlist()
        expected = {1: {'user_id': 1, 'name': 'Hiking', 'description': 'Go for hiking'}}
        self.assertNotEqual(expected, result)

    def test_successful_bucketlist_creation(self):
        """Test bucketlist creation is successful"""
        result = self.bucketlist.create_bucketlist()
        expected = {1: {'user_id': 1, 'name': 'Hiking', 'description': 'Go for hiking'}}
        self.assertEqual(expected, result)


class ActivityTestCase(unittest.TestCase):
    """ Test the BucketlistItem class """

    def setUp(self):
        """ Setup a bucketlist """
        User.users = {1: {'leo@email.com', 'leo', 'pwd'}}
        Bucketlist.bucketlists = {1: {'user_id': 1, 'name': 'Hiking', 'description': 'Go for hiking'}}
        Activity.activities = {}
        self.activity = Activity('Hiking', 'Go for hiking', True)

    def tearDown(self):
        del self.activity
        del Bucketlist.bucketlists
        del User.users

    def test_successful_activity_creation(self):
        """Test bucketlist item creation is successful"""
        result = self.activity.create_activity()
        expected = {3: {'bucketlist_id': 0, 'title': 'Hiking', 'description': 'Go for hiking', 'status': True}}
        self.assertEqual(expected, result)

    def test_show_activities_without_login_redirects(self):
        """Users need valid credentials"""
        User.users = {}
        tester = app.test_client(self)
        response = tester.post('/show_bucketlists', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_activities_dashboard_without_login_redirects(self):
        """Users need valid credentials"""
        User.users = {}
        tester = app.test_client(self)
        response = tester.get('/show_activities', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
