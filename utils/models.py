from flask_login import UserMixin
from api.api import find_user
import bcrypt


class User(UserMixin):
    def __init__(self, name, email, salt=None, pw_hash=None, pw=None):
        """
        :param name:    Username
        :param email:   Email
        :param salt:    User password salt
        :param pw_hash: User password hash
        :param pw:      User pure password (for new Users)
        """
        self.name = name
        self.name_lower = name.lower()
        self.email = email.lower()

        if pw is not None:
            self.set_password(pw)
        else:
            self.salt = salt
            self.pw_hash = pw_hash

    @staticmethod
    def get_user(username, email=False):
        """
        Get existing User by calling the database
        :param username: Username/Email to query
        :param email:    True if we want to query by email
        :return:         None or User object
        """

        user = find_user(username, email)

        if user is None:
            return None

        name = user["_id"]
        email = user["email"]
        salt = user["password"]["salt"]
        pw_hash = user["password"]["hashed"]

        u = User(name, email, salt=salt, pw_hash=pw_hash)
        return u

    def check_password(self, password):
        """
        Checks if the User password is correct
        :param password: Password to check
        :return:         True if hash matches, otherwise False
        """

        return bcrypt.checkpw(password.encode('utf8'), self.pw_hash)

    def set_password(self, password):
        """
        Sets the password of the User
        :param password: Password to set
        """

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf8'), salt)

        self.salt = salt
        self.pw_hash = hashed

    def get_id(self):
        return self.name
