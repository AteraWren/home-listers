import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from .config import Config

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
jwt = JWTManager()  # Create an instance of JWTManager

def create_app(config_class=None):
    """
    Create and configure the Flask application.

    Args:
        config_class (class, optional): The configuration class to use. Defaults to `Config`.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class or Config)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)

    # Import and register blueprints
    from .routes import routes as routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app