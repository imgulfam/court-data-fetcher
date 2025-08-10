import os

# Find the absolute path of the directory where this file is located
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Base configuration class. Contains default configuration settings + configuration settings applicable to all environments.
    """
    # Default settings
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    
    # Settings applicable to all environments
    SECRET_KEY = os.getenv('SECRET_KEY', default='a-very-secret-key-that-you-should-change')
    
    # Database configuration
    # The 'instance' folder is a good place for the database file as it's not part of the app package.
    # Flask knows about this folder, and we've added it to .gitignore.
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', default=f"sqlite:///{os.path.join(basedir, 'instance', 'site.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False