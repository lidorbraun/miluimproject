import os

DB_USER = "postgres"
DB_PASSWORD = "d&eZ_'ORAEi<rLM=gr"
DB_NAME = "document_system"
DB_HOST = "localhost"
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

SQLALCHEMY_TRACK_MODIFICATIONS = False


class Config:
    SECRET_KEY = "f6594a8604d44e033644531b7a479693fb0bb6f9b916d9b00673fd6edbbc6427"  # Change this for security
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = UPLOAD_FOLDER






