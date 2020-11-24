import os

# setting a secret key for hashing
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-password'