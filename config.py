from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    FLASK_APP = environ.get('FLASK_APP')
    SECRET_KEY = environ.get('SECRET_KEY')

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    TESTING = True
    FLASK_ENV = 'development'
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI_LOCAL")


class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
