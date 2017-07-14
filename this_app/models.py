class User(object):
    """Represents a user who can Create, Read, Update & Delete his own bucketlists"""

    user_id = 0
    users = {}
    user_bucketlists = {}

    def __init__(self, email, username, password):
        """Constructor to initialize class"""

        User.user_id += 1    # This line is a game changer
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
    """Represents a class to Create, Read, Update & Delete a bucketlist"""

    buck_id = 0
    bucketlists = {}
    bucketlist_items = {}

    def __init__(self, name, description):
        """Constructor to initialize class"""

        Bucketlist.buck_id += 1    # Alter the outside class var buck_id, NB: self.buck_id works but replaces items instead of updating the dict
        self.name = name
        self.description = description


    def create_bucketlist(self):
        """ Class to create and store a bucketlist object """

        Bucketlist.bucketlists.update({
            Bucketlist.buck_id: {
                'name': self.name,
                'description': self.description
            }
        })
        
        return self

    def insert_into_user(self):
        """ Give the created bucketlist to its owner """
        User.user_bucketlists.update({
            User.user_id: Bucketlist.bucketlists
        })


class BucketlistItem(object):
    """Represents a class to Create, Read, Update & Delete bucketlist items"""

    item_id = 0
    bucketlist_items = {}

    def __init__(self, title, description, status=True):
        """Constructor to initialize class"""

        BucketlistItem.item_id += 1
        self.name = title
        self.description = description
        self.status = status


    def create_bucketlist_item(self):
        """ Class to create and store a bucketlist item """

        self.bucketlist_items.update({
            self.item_id: {
                'name': self.name,
                'description': self.description,
                'status': self.status
            }
        })
        
        return self

    def insert_into_bucketlist(self):
        """ Give the created bucketlist item to its bucketlist """
        Bucketlist.bucketlist_items.update({
            User.user_id: BucketlistItem.bucketlist_items
        })
