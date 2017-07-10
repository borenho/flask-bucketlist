from werkzeug.security import generate_password_hash, check_password_hash

class User(object):
    """represents a user who can CRUD his own bucketlists"""

    users = {}

    def __init__(self, email, username, password):
        """Constructor class to initialize class"""

        self.email = email
        self.username = username
        self.password = generate_password_hash(password)


    def create_user(self):
        """ Class to create and store a user object """

        self.users.update({
            self.email: {
                'email': self.email,
                'username': self.username,
                'password': self.password
            }
        })

        return self.users
