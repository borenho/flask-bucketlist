class User(object):
    """Represents a user who can Create, Read, Update & Delete his own bucketlists"""

    user_id = 0
    users = {}
    user_bucketlists = {}

    def __init__(self, email, username, password):
        """Constructor class to initialize class"""

        self.user_id += 1
        self.email = email
        self.username = username
        self.password = password


    def create_user(self):
        """ Class to create and store a user object """

        self.users.update({
            self.user_id: {
                'email': self.email,
                'username': self.username,
                'password': self.password
            }
        })

        return self


class Bucketlist(object):
    """Represents a user who can Create, Read, Update & Delete his own bucketlists"""

    buck_id = 0
    bucketlists = {}

    def __init__(self, name, description):
        """Constructor class to initialize class"""

        self.buck_id += 1
        self.name = name
        self.description = description
        self.bucketlist_items = {}


    def create_bucketlist(self):
        """ Class to create and store a bucketlist object """

        self.bucketlists.update({
            self.buck_id: {
                'name': self.name,
                'description': self.description
            }
        })
        
        return self

    def insert_into_user(self):
        """ Give the created bucketlist to its owner """
        User.user_bucketlists.update({
            User.user_id: self.bucketlists
        })
