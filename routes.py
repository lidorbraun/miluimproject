from flask import render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db, Document, Request, Message
from forms import RegistrationForm, LoginForm, UploadForm, UpdatePasswordForm, CommentForm, MessageForm
from app import app
import os


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = RegistrationForm()

    if form.validate_on_submit():
        print("✅ Form validated successfully!")  # Debugging

        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)

        try:
            db.session.add(user)
            db.session.commit()
            print(f"✅ User {user.username} added to the database.")  # Debugging
            flash("Account created successfully! You can now log in.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            db.session.rollback()
            print(f"❌ Database Error: {e}")  # Debugging
            flash("Database error! Please try again.", "danger")

    else:
        print("❌ Form validation failed!")  # Debugging
        print(form.errors)  # This will show form validation errors

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))  # Redirect if already logged in

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password.", "danger")

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    form = CommentForm()  # Create an instance of the form

    if current_user.role == "Student":
        documents = Document.query.filter_by(student_id=current_user.id).all()
    elif current_user.role == "Lecturer":
        documents = Document.query.filter_by(status="Pending").all()
    elif current_user.role == "Reviewer":
        documents = Document.query.all()  # Reviewers can see all documents
    else:
        documents = []

    return render_template("dashboard.html", documents=documents, user=current_user, form=form)


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload_document():
    if current_user.role != "Student":
        flash("רק סטודנטים יכולים להעלות מסמכים.", "danger")
        return redirect(url_for("dashboard"))

    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        original_filename = file.filename
        filename = secure_filename(original_filename)

        # Extract the file extension and ensure it's included
        file_extension = os.path.splitext(original_filename)[1]  # Gets ".pdf" or ".docx"
        if not file_extension:
            flash("שגיאה: לא ניתן לזהות את סוג הקובץ.", "danger")
            return redirect(url_for("upload_document"))

        # Ensure the file saves with its correct extension
        saved_filename = filename if filename.endswith(file_extension) else filename + file_extension
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], saved_filename)

        file.save(file_path)  # Save file correctly

        # Save file record in database
        document = Document(
            title=form.title.data,
            file_path=saved_filename,  # Store only the filename, not full path
            student_id=current_user.id
        )

        db.session.add(document)
        db.session.commit()

        flash("המסמך הועלה בהצלחה!", "success")
        return redirect(url_for("dashboard"))

    return render_template("upload.html", form=form)


@app.route("/uploads/<filename>")
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)


@app.route("/approve_document/<int:document_id>", methods=["POST"])
@login_required
def approve_document(document_id):
    if current_user.role != "Lecturer":
        flash("רק מרצים יכולים לאשר או לדחות מסמכים.", "danger")
        return redirect(url_for("dashboard"))

    document = Document.query.get_or_404(document_id)
    action = request.form.get("action")

    if action == "approve":
        document.status = "Approved"
    elif action == "reject":
        document.status = "Rejected"

    db.session.commit()
    flash("סטטוס המסמך עודכן בהצלחה!", "success")
    return redirect(url_for("dashboard"))


@app.route("/update_password", methods=["GET", "POST"])
@login_required
def update_password():
    form = UpdatePasswordForm()

    if form.validate_on_submit():
        user = current_user

        if not check_password_hash(user.password_hash, form.old_password.data):
            flash("סיסמה נוכחית שגויה.", "danger")
            return redirect(url_for("update_password"))

        user.set_password(form.new_password.data)
        db.session.commit()
        flash("סיסמה עודכנה בהצלחה!", "success")
        return redirect(url_for("dashboard"))

    return render_template("update_password.html", form=form)


@app.route("/add_comment/<int:document_id>", methods=["POST"])
@login_required
def add_comment(document_id):
    if current_user.role != "Lecturer":
        flash("רק מרצים יכולים להוסיף הערות.", "danger")
        return redirect(url_for("dashboard"))

    document = Document.query.get_or_404(document_id)
    comment_text = request.form.get("comment")

    if comment_text:
        document.comments = comment_text  # Save comment in the database
        db.session.commit()
        flash("ההערה נוספה בהצלחה!", "success")
    else:
        flash("לא ניתן להוסיף הערה ריקה.", "warning")

    return redirect(url_for("dashboard"))


@app.route("/review_approve/<int:document_id>", methods=["POST"])
@login_required
def review_approve(document_id):
    if current_user.role != "Reviewer":
        flash("רק בקרים יכולים לאשר או לדחות מסמכים.", "danger")
        return redirect(url_for("dashboard"))

    document = Document.query.get_or_404(document_id)
    action = request.form.get("action")

    if action == "approve":
        document.status = "Approved"
    elif action == "reject":
        document.status = "Rejected"

    db.session.commit()
    flash("סטטוס המסמך עודכן בהצלחה!", "success")
    return redirect(url_for("dashboard"))


@app.route("/messages", methods=["GET"])
@login_required
def messages():
    received_messages = Message.query.filter_by(receiver_id=current_user.id).order_by(Message.sent_at.desc()).all()
    sent_messages = Message.query.filter_by(sender_id=current_user.id).order_by(Message.sent_at.desc()).all()
    return render_template("messages.html", received_messages=received_messages, sent_messages=sent_messages)


@app.route("/send_message", methods=["GET", "POST"])
@login_required
def send_message():
    form = MessageForm()

    if form.validate_on_submit():
        recipient = User.query.filter_by(username=form.receiver.data).first()
        if not recipient:
            flash("המשתמש לא נמצא.", "danger")
            return redirect(url_for("send_message"))

        message = Message(
            sender_id=current_user.id,
            receiver_id=recipient.id,
            subject=form.subject.data,
            message=form.message.data
        )

        db.session.add(message)
        db.session.commit()
        flash("ההודעה נשלחה בהצלחה!", "success")
        return redirect(url_for("messages"))

    return render_template("send_message.html", form=form)




