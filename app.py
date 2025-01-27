from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect unauthorized users to login

from models import User
from routes import *  # Import routes at the end

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))





if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)