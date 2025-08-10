import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    """
    Creates and configures an instance of the Flask application.
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config_class)
    
    db.init_app(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        # Import parts of our application
        from . import models # This line was already here
        from .routes import main_routes # <-- NEW LINE

        # Register Blueprints
        app.register_blueprint(main_routes) # <-- NEW LINE
        
        # Create database tables for our models
        db.create_all() # This line was already here

    return app