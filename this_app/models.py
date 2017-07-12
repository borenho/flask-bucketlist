from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
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

        return self.users

    @property
    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the id """
        users_dict = self.users.items()
        user = {key:value for key, value in users_dict}
        return str(user.keys())

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
