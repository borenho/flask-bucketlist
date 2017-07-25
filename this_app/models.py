from werkzeug.security import generate_password_hash
from flask import session, request

class User(object):
    """Represents a user who can Create, Read, Update & Delete his own bucketlists"""

    user_id = 0
    users = {}

    def __init__(self, email, username, password):
        """Constructor to initialize class"""

        User.user_id += 1    # This line is a game changer
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)


    def create_user(self):
        """ Class to create and store a user object """

        self.users.update({
            self.user_id: {
                'email': self.email,
                'username': self.username,
                'password': self.password
            }
        })

        return self.users


class Bucketlist(object):
    """Represents a class to Create, Read, Update & Delete a bucketlist"""

    buck_id = 0
    bucketlists = {}

    def __init__(self, name, description):
        """Constructor to initialize class"""

        Bucketlist.buck_id += 1    # Alter the outside class var buck_id, NB: self.buck_id works but replaces items instead of updating the dict
        self.name = name
        self.description = description


    def create_bucketlist(self):
        """ Class to create and store a bucketlist object """

        self.bucketlists.update({
            self.buck_id: {'user_id': User.user_id, 'name': self.name, 'description': self.description}
        })

        global bucketlists
        return self.bucketlists
        

    def add_bucketlist(self):
        """ Add bucketlist to a list with an existing bucketlist """
        # First get the user id from existing bucketlist
        bucketlist_dict = Bucketlist.bucketlists.items()
        for k, v in bucketlist_dict:
            existing_owner = v['user_id']

        self.bucketlists.update({
            self.buck_id: {'user_id': existing_owner, 'name': self.name, 'description': self.description}
        })

        return self.bucketlists

    def edit_bucketlist(self):
        """
        Class to edit bucketlist
        """
        bucketlists_dict = Bucketlist.bucketlists.items()
        user_bucketlists = {k:v for k, v in bucketlists_dict if session['user_id']==v['user_id']}
        bucketlist = {k:v for k, v in user_bucketlists.items() if k==int(request.form['key'])}
        print('To be edited =', bucketlist)
        for k, v in bucketlist.items():
            existing_owner = v['user_id']
            bucketlist[k] = {'user_id': existing_owner, 'name': self.name, 'description': self.description}

            print('Should have been edited =', bucketlist)
            global bucketlist
            return bucketlist

    def get_all(self):
        """
        Gets all the bucketlists created by a logged in user
        """
        pass

    def delete_bucketlist(self, id):
        """
        Deletes a single bucketlist created by a logged in user
        """
        # Retrieve a user's bucketlist using it's ID
        bucketlists_dict = Bucketlist.bucketlists.items()
        user_bucketlists = {k:v for k, v in bucketlists_dict if session['user_id']==v['user_id']}
        bucketlist = {k:v for k, v in user_bucketlists.items() if id==k}

        del bucketlist
        global user_bucketlists
        return user_bucketlists


class Activity(object):
    """Represents a class to Create, Read, Update & Delete bucketlist items"""

    activity_id = 0
    activities = {}

    def __init__(self, title, description, status):
        """Constructor to initialize class"""

        Activity.activity_id += 1
        self.title = title
        self.description = description
        self.status = status

    def create_activity(self):
        """ Class to create and store a bucketlist item """

        self.activities.update({
            self.activity_id: {
                'bucketlist_id': Bucketlist.buck_id,
                'title': self.title,
                'description': self.description,
                'status': self.status
            }
        })
        
        return self.activities

    def edit_activity(self):
        """ Class to edit bucketlist """

        # Get the key and update the values
        activity_dict = Activity.activities
        print('edit activity -', activity_dict)
        if len(activity_dict) > 1:
            activity = {k:v for k, v in activity_dict.items() if session['activity_id']==k}
            for key in activity:
                if session['activity_id']==key:
                    for k, v in activity.items():
                        bucket = v['bucketlist_id']
                        activity[key] = {'bucketlist_id': bucket, 'title': self.title, 'description': self.description, 'status': self.status}

                        return activity

        # Use different logic if one item present in dict
        else:
            for key in activity_dict:
                if session['activity_id']==key:
                    for k, v in activity_dict.items():
                        bucket = v['bucketlist_id']
                        activity_dict[key] = {'bucketlist_id': bucket, 'title': self.title, 'description': self.description, 'status': self.status}

                        return activity_dict
