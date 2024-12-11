from werkzeug.security import generate_password_hash
from models import User, db
from app import create_app  # Import the create_app function

# Initialize the Flask app
app = create_app()

# Use the app context for database operations
with app.app_context():
    # Create an admin user
    hashed_password = generate_password_hash("atp")  # Replace with a strong password
    admin_user = User(
        name="Super Admin",
        email="a@a.com",
        password=hashed_password,
        address="Admin HQ",
        is_admin=True
    )
    db.session.add(admin_user)
    db.session.commit()
    print("Admin user created successfully!")
