from flask import session, request
from werkzeug.security import generate_password_hash

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

        return self.bucketlists


    def edit_bucketlist(self):
        """
        Class to edit bucketlist
        """
        bucketlists_dict = Bucketlist.bucketlists
        for item in bucketlists_dict.values():
            if session['user_id'] == item['user_id']:
                for key, val in bucketlists_dict.items():
                    if key == int(request.form['key']):
                        print('To be edited =', bucketlists_dict[key])
                        existing_owner = val['user_id']
                        bucketlists_dict[key] = {'user_id': existing_owner, 'name': self.name, 'description': self.description}

                        return bucketlists_dict

    @staticmethod
    def get_all():
        """
        Gets all the bucketlists created by a logged in user
        """
        print ('User bucketlists')
        
        all_bucketlists = Bucketlist.bucketlists.items()
        user_bucketlists = {k:v for k, v in all_bucketlists if session['user_id']==v['user_id']}

        return user_bucketlists

    @staticmethod
    def delete_bucketlist():
        """
        Deletes a single bucketlist created by a logged in user
        """
        # Retrieve a user's bucketlist using it's ID
        bucketlists_dict = Bucketlist.bucketlists
        for item in bucketlists_dict.values():
            if session['user_id'] == item['user_id']:
                for key in bucketlists_dict:
                    if key == int(request.form['key']):
                        print('To be deleted =', bucketlists_dict[key])
                        del bucketlists_dict[key]

                        print('Should have been deleted =', bucketlists_dict)

                        return bucketlists_dict


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

    def create_activity(self, bucketlist_id):
        """ Class to create and store a bucketlist item """

        self.activities.update({
            self.activity_id: {
                'bucketlist_id': bucketlist_id,
                'title': self.title,
                'description': self.description,
                'status': self.status
            }
        })
        
        return self.activities

    def edit_activity(self, bucketlist_id, key):
        """
        Class to edit activities
        """
        all_activities = Activity.activities
        for k, val in all_activities.items():
            if k == key and val['bucketlist_id'] == bucketlist_id:
                print('To be edited =', all_activities[k])
                parent_bucketlist = val['bucketlist_id']
                all_activities[k] = {'bucketlist_id': parent_bucketlist, 'title': self.title, 'description': self.description, 'status': self.status}

                print('Should have been edited =', all_activities)

                return all_activities

    @staticmethod
    def get_all():
        """
        Gets all the activities created by a logged in user
        """
        print ('User activities')
        
        all_activities = Activity.activities.items()
        user_activities = {k:v for k, v in all_activities if session['user_id']==v['user_id']}
        # Now get the activities belonging to a particular bucketlist
        buck_activities = {k:v for k, v in user_activities if session['bucketlist_id']==v['bucketlist_id']}


        return buck_activities

    @staticmethod
    def delete_activity(bucketlist_id, key):
        """
        Deletes a single bucketlist created by a logged in user
        """
        print('Passing')
        print('Key', key)
        all_activities = Activity.activities
        for item in all_activities.values():
            if bucketlist_id == item['bucketlist_id']:
                for k in all_activities:
                    if k == key:
                        print('To be deleted =', all_activities[key])
                        del all_activities[key]

                        print('Should have been deleted =', all_activities)

                        return all_activities
