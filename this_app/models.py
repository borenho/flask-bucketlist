from werkzeug.security import generate_password_hash, check_password_hash

class User(object):
    """Represents a user who can Create, Read, Update & Delete his own bucketlists"""

    counter = 0
    users = {}

    def __init__(self, email, username, password):
        """Constructor class to initialize class"""

        self.email = email
        self.username = username
        self.password = password
        User.counter += 1


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
