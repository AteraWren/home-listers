from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from .config import Config
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])
    print("Secret Key:", app.config['SECRET_KEY'])

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from .models import User, Post
    from .routes import routes as routes_blueprint
    app.register_blueprint(routes_blueprint)

    print("App and SQLAlchemy instance initialized")
    print("App instance:", app)
    print("SQLAlchemy instance:", db)

    return app

from . import db, bcrypt  # Import the db and bcrypt instances from the main application file
from . import login_manager  # Import the LoginManager instance

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Add this method to display meaningful information
    def __repr__(self):
        return f"<Post {self.id}: {self.title}, {self.location}, ${self.price}>"