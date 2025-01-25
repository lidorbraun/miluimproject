from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    role = SelectField("Role", choices=[("Student", "Student"), ("Lecturer", "Lecturer"), ("Reviewer", "Reviewer")],
                       validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class UploadForm(FlaskForm):
    title = StringField("כותרת המסמך", validators=[DataRequired()])
    file = FileField("בחר קובץ", validators=[DataRequired(), FileAllowed(['pdf', 'docx'])])
    submit = SubmitField("העלה מסמך")


class UpdatePasswordForm(FlaskForm):
    old_password = PasswordField("סיסמה נוכחית", validators=[DataRequired()])
    new_password = PasswordField("סיסמה חדשה", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("אישור סיסמה חדשה", validators=[DataRequired(), EqualTo("new_password")])
    submit = SubmitField("עדכן סיסמה")


class CommentForm(FlaskForm):
    comment = TextAreaField("הוסף הערה", validators=[DataRequired(), Length(max=500)])
    submit = SubmitField("שמור הערה")


class MessageForm(FlaskForm):
    receiver = StringField("נמען", validators=[DataRequired()])
    subject = StringField("נושא", validators=[DataRequired()])
    message = TextAreaField("הודעה", validators=[DataRequired()])
    submit = SubmitField("שלח הודעה")


class ReviewForm(FlaskForm):
    rating = IntegerField("דירוג (1-5)", validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField("הערה", validators=[DataRequired()])
    submit = SubmitField("שלח ביקורת")
