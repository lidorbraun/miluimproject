from models import db, User
from app import app

with app.app_context():
    try:
        users = User.query.all()
        print(f"✅ Connected! Found {len(users)} users in the database.")
    except Exception as e:
        print(f"❌ Database connection error: {e}")
