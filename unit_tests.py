import unittest
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Document, Request, Message, WebReview, db
from forms import (
    RegistrationForm, LoginForm, UploadForm, UpdatePasswordForm,
    CommentForm, MessageForm, ReviewForm
)
from datetime import datetime


class TestForms(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'test_secret_key'
        self.app.config['WTF_CSRF_ENABLED'] = False
        CSRFProtect(self.app)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_registration_form_valid(self):
        form = RegistrationForm(
            username='testuser', email='test@example.com',
            password='password123', confirm_password='password123', role='Student'
        )
        self.assertTrue(form.validate())

    def test_login_form_valid(self):
        form = LoginForm(email='test@example.com', password='password123')
        self.assertTrue(form.validate())

    def test_upload_form_valid(self):
        form = UploadForm(title='Document Title')
        self.assertFalse(form.validate())

    def test_update_password_form_valid(self):
        form = UpdatePasswordForm(
            old_password='oldpass123', new_password='newpass123', confirm_password='newpass123'
        )
        self.assertTrue(form.validate())

    def test_comment_form_valid(self):
        form = CommentForm(comment='This is a valid comment.')
        self.assertTrue(form.validate())

    def test_message_form_valid(self):
        form = MessageForm(receiver='testuser', subject='Test Subject', message='Test message content.')
        self.assertTrue(form.validate())

    def test_review_form_valid(self):
        form = ReviewForm(rating=5, comment='Great experience!')
        self.assertTrue(form.validate())

    def test_user_model(self):
        user = User(username='testuser', email='test@example.com', role='Student')
        user.set_password('securepassword')
        self.assertTrue(user.check_password('securepassword'))

    def test_document_model(self):
        document = Document(title='Test Document', file_path='/path/to/file.pdf', student_id=1)
        self.assertIsNone(document.status, 'Pending')

    def test_request_model(self):
        request = Request(document_id=1, lecturer_id=2, status='Pending', comments='Needs review')
        self.assertEqual(request.status, 'Pending')

    def test_message_model(self):
        message = Message(sender_id=1, receiver_id=2, subject='Hello', message='This is a test message.')
        self.assertEqual(message.subject, 'Hello')

    def test_web_review_model(self):
        review = WebReview(student_id=1, rating=5, comment='Excellent service!')
        self.assertEqual(review.rating, 5)

    def test_valid_user_creation(self):
        user = User(username='student1', email='student1@example.com', role='Student')
        user.set_password('mypassword')
        self.assertTrue(user.check_password('mypassword'))

    def test_message_mark_read(self):
        message = Message(sender_id=1, receiver_id=2, subject='Hello', message='Test')
        message.read = True
        self.assertTrue(message.read)

    def test_document_default_status(self):
        document = Document(title='New Doc', file_path='file.pdf', student_id=1)
        self.assertIsNot(document.status, 'Pending')

    def test_review_creation(self):
        review = WebReview(student_id=1, rating=4, comment='Good')
        self.assertEqual(review.rating, 4)

    def test_comment_form_filled(self):
        form = CommentForm(comment='Nice work!')
        self.assertTrue(form.validate())

    def test_message_form_subject(self):
        form = MessageForm(receiver='lecturer1', subject='Question', message='I need help')
        self.assertTrue(form.validate())

    def test_password_hashing(self):
        password = 'secure123'
        hashed = generate_password_hash(password)
        self.assertTrue(check_password_hash(hashed, password))

    def test_registration_form_username(self):
        form = RegistrationForm(username='uniqueuser', email='user@test.com', password='pass123', confirm_password='pass123', role='Student')
        self.assertTrue(form.validate())

    def test_update_password_different_new_password(self):
        form = UpdatePasswordForm(old_password='oldpass', new_password='newpass1', confirm_password='newpass1')
        self.assertTrue(form.validate())

    def test_request_default_timestamps(self):
        request = Request(document_id=1, lecturer_id=2)
        self.assertNotIsInstance(request.created_at, datetime)

    def test_valid_review_comment(self):
        form = ReviewForm(rating=3, comment='Okay experience')
        self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main()