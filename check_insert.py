from models import db, User
from app import app

with app.app_context():
    try:
        user = User(username="testuser", email="test@example.com", role="Student")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        print("✅ Test user added successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error adding user: {e}")