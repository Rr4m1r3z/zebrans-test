import os
from datetime import timedelta

SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(os.environ['USERZEBRAND'],os.environ['PASSZEBRAND'],os.environ['HOSTZEBRAND'],os.environ['BASEZEBRAND'])

# Turn off the Flask-SQLAlchemy event system and warning
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_EXPIRATION_DELTA = timedelta(seconds=43200)