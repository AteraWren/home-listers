from backend import create_app, db
from backend.models import User

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
        print(f"Password for user '{email}' has been reset.")
    else:
        print(f"User with email '{email}' not found.")