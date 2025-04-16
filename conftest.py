import pytest
from backend import create_app, db
# from dotenv import load_dotenv
import os

# Load environment variables from .env
# load_dotenv()

@pytest.fixture
def app():
    # Explicitly unset DATABASE_URL to ensure it doesn't interfere
    os.environ.pop('DATABASE_URL', None)
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'  # Override DATABASE_URL for tests

    app = create_app(config_class='backend.config.TestConfig')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Explicitly set the test database

    print(f"Using DATABASE_URL: {os.getenv('DATABASE_URL')}")  # Debugging
    print(f"App Config DATABASE_URL: {app.config['SQLALCHEMY_DATABASE_URI']}")  # Debugging

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()