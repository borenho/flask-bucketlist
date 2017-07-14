class User(object):
    """Represents a user who can Create, Read, Update & Delete his own bucketlists"""

    counter = 0
    users = {}

    def __init__(self, email, username, password):
        """Constructor class to initialize class"""

        User.counter += 1
        self.email = email
        self.username = username
        self.password = password
        self.bucketlists = {}


    def create_user(self):
        """ Class to create and store a user object """

        self.users.update({
            self.counter: {
                'email': self.email,
                'username': self.username,
                'password': self.password
            }
        })

        return self


class Bucketlist(object):
    """Represents a user who can Create, Read, Update & Delete his own bucketlists"""

    counter = 0
    bucketlists = {}

    def __init__(self, name, description):
        """Constructor class to initialize class"""

        Bucketlist.counter += 1
        self.name = name
        self.description = description
        self.bucketlist_items = {}


    def create_bucketlist(self):
        """ Class to create and store a bucketlist object """

        self.bucketlists.update({
            self.counter: {
                'name': self.name,
                'description': self.description
            }
        })

        return self

    def insert_into_user(self):
        """ Give the created bucketlist to its owner """
        pass
