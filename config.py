""" Configuration file """
import os

SECRET_KEY = os.getenv('KEY', 'something_really_secret')
DEBUG = os.getenv('DEBUG', True)

SQLALCHEMY_DATABASE_URI = 'sqlite:///Novy_dvor.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
