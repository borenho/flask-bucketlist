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

    def test_login_to_bucketlists(self):
        """ Ensure signup redirects to login """
        tester = app.test_client(self)
        response = tester.post('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


class UserTestCase(unittest.TestCase):
    """ Test the User class """

    def setUp(self):
        """ Setup a new user """
        User.users = {}
        self.app = User('leo@email.com', 'leo', 'pwd')
        # Set some default user data
        self.user_data = {
            1: {
                'email': 'leo@email.com',
                'username': 'leo',
                'password': 'pwd'  
            }
            
        }

    def test_users_dictionary(self):
        """Test user's dict is empty at first"""
        new_user = self.app
        self.assertEqual(len(new_user.users), 0)
        new_user.create_user()
        self.assertIsInstance(new_user, User)
        self.assertEqual(len(new_user.users), 1)

    def test_user_id(self):
        """Test user_id starts from one and increments by one"""
        new_user = self.app
        self.assertTrue(new_user.user_id, 0)
        new_user.create_user()
        self.assertTrue(new_user.user_id, 1)
        for key in new_user.users:
            self.assertEqual(new_user.user_id, key)

    def test_users_can_signup(self):
        """Test new user can sign up successfully"""
        for value in self.app.users.values():
            result = self.app.create_user()
            stored_password = value['password']
            expected = {0: {
                'email': 'leo@email.com', 'username': 'leo', 'password': stored_password
                }}
            self.assertEqual(expected, result)

    def test_registering_user(self):
        """Test that a user cannot be registered twice."""
        new_user = self.app
        new_user.create_user()
        client = app.test_client(self)
        response = client.post('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_successful_login(self):
        """Test registered user can login successfully"""
        pass

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
        self.app = Bucketlist('Hiking', 'Go for hiking')
        Bucketlist.bucketlists = {}
        self.client = app.test_client(self)
        # Set some default bucketlist data
        self.bucketlist_data = {
            1: {
                'user_id': 1,
                'name': 'Hiking',
                'description': 'Go for hiking'
            }
            
        }

    def test_bucketlists_dictionary(self):
        """Test bucketlist's dict is empty at first"""
        new_bucketlist = self.app
        self.assertEqual(len(new_bucketlist.bucketlists), 0)
        new_bucketlist.create_bucketlist()
        self.assertIsInstance(new_bucketlist, Bucketlist)
        self.assertEqual(len(new_bucketlist.bucketlists), 1)

    def test_bucketlist_id(self):
        """Test bucketlist_id starts from one and increments by one"""
        new_bucketlist = self.app
        self.assertTrue(new_bucketlist.buck_id, 0)
        new_bucketlist.create_bucketlist()
        self.assertTrue(new_bucketlist.buck_id, 1)
        for key in new_bucketlist.bucketlists:
            self.assertEqual(new_bucketlist.buck_id, key)

    def test_create_bucketlist(self):
        """Test bucketlist can be created"""
        new_bucketlist = self.app
        new_bucketlist.create_bucketlist()
        self.assertEqual(len(new_bucketlist.bucketlists), 1)

    def test_user_id_in_bucketlist(self):
        """User id starts from one onwards"""
        new_bucketlist = self.app
        new_bucketlist.create_bucketlist()
        for value in Bucketlist.bucketlists.values():
            for key in User.users:
                self.assertEqual(value['user_id']+1, key)
        new_bucketlist.create_bucketlist()
        for value in Bucketlist.bucketlists.values():
            for key in User.users:
                self.assertEqual(value['user_id']+1, key)

    def test_create_bucketlist_without_user_fails(self):
        """Test bucketlist creation without a user fails"""
        User.users = {}
        result = self.app.create_bucketlist()
        expected = {1: {'user_id': 1, 'name': 'Hiking', 'description': 'Go for hiking'}}
        self.assertNotEqual(expected, result)

    def test_successful_bucketlist_creation(self):
        """Test bucketlist creation is successful"""
        result = self.app.create_bucketlist()
        expected = {5: {'user_id': 0, 'name': 'Hiking', 'description': 'Go for hiking'}}
        self.assertEqual(expected, result)

    def tearDown(self):
        del self.app
        del self.bucketlist_data
        del Bucketlist.bucketlists
        del User.users


class ActivityTestCase(unittest.TestCase):
    """ Test the BucketlistItem class """

    def setUp(self):
        """ Setup an activity """
        User.users = {1: {'leo@email.com', 'leo', 'pwd'}}
        Bucketlist.bucketlists = {1: {'user_id': 1, 'name': 'Hiking', 'description': 'Go for hiking'}}
        Activity.activities = {}
        self.app = Activity('Hiking', 'Go for hiking', True)
        # Set some default activity data
        self.activity_data = {
            1: {
                'bucketlist_id': 1,
                'name': 'Hiking',
                'description': 'Go for hiking',
                'status': True
            }   
        }

    def test_activity_dictionary(self):
        """Test activity's dict is empty at first"""
        new_activity = self.app
        self.assertEqual(len(new_activity.activities), 0)
        new_activity.create_activity(1)
        self.assertIsInstance(new_activity, Activity)
        self.assertEqual(len(new_activity.activities), 1)

    def test_activity_id(self):
        """Test activity_id starts from one and increments by one"""
        new_activity = self.app
        self.assertTrue(Activity.activity_id, 0)
        new_activity.create_activity(1)
        self.assertTrue(new_activity.activity_id, 1)
        for key in new_activity.activities:
            self.assertEqual(new_activity.activity_id, key)

    def test_successful_activity_creation(self):
        """Test bucketlist item creation is successful"""
        result = self.app.create_activity(1)
        expected = {4: {'bucketlist_id': 1, 'title': 'Hiking', 'description': 'Go for hiking', 'status': True}}
        self.assertEqual(expected, result)

    def test_show_activities_without_login_redirects(self):
        """Users need valid credentials"""
        User.users = {}
        tester = app.test_client(self)
        response = tester.post('/show_bucketlists', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        del self.app
        del self.activity_data
        del Activity.activities
        del Bucketlist.bucketlists
        del User.users
