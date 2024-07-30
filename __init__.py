from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_socketio import SocketIO
from .models import load_user
from .utils import db  # Import the db instance from utils

# Import blueprints
from .routes import auth
from .routes import main

login_manager = LoginManager()
login_manager.user_loader = load_user

socketio = SocketIO()


def create_database(app):
    """Creates all database tables."""
    with app.app_context():
        db.create_all()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Placeholder, update after choosing a database
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'  # Remember to create this folder

    # Initialize dependencies
    login_manager.init_app(app)
    db.init_app(app)  # Use the imported db instance
    CORS(app)
    socketio.init_app(app)

    # Create database tables
    create_database(app)

    # Register blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(main)

    return app
