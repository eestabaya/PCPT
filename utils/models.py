"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

#user loader is registered with Flask-Login with the @login.user_loader
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db_name.Model):
    # ...

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class User(UserMixin, db_name.Model):
"""