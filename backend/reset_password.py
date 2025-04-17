"""
Reset a user's password.

This script resets the password for a specific user in the database.
"""

from backend import create_app, db
from backend.models import User
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

with app.app_context():
    # Find the user by email
    email = "traveldreamer@example.com"  # Replace with the user's email
    user = User.query.filter_by(email=email).first()

    if user:
        # Reset the password
        new_password = "DreamBig2025"  # Replace with the new password
        user.set_password(new_password)
        db.session.commit()
        logger.info("Password has been reset for the specified user.")  # Log without exposing sensitive data
    else:
        logger.warning("User not found for the specified email.")  # Log without exposing sensitive data