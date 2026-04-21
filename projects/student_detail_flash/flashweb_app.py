"""
Student Management System — Flask App
Run: python app.py
"""

import re
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# ── App & DB config ──────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "student_system_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ── Models ───────────────────────────────────────────────────────────────────

class User(db.Model):
    """Registered users (admin accounts)."""
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(100), nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    phone    = db.Column(db.String(15),  nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Student(db.Model):
    """Student records managed by users."""
    id     = db.Column(db.Integer, primary_key=True)
    name   = db.Column(db.String(100), nullable=False)
    email  = db.Column(db.String(120), unique=True, nullable=False)
    course = db.Column(db.String(100), nullable=False)
    phone  = db.Column(db.String(15),  nullable=False)


# ── Helpers ──────────────────────────────────────────────────────────────────

def login_required(f):
    """Decorator — redirect to login if not authenticated."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login to continue.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


def validate_password(password):
    """
    Returns True if password meets rules:
    - 8–14 characters
    - At least 1 uppercase, 1 lowercase, 1 digit, 1 special character
    """
    if not (8 <= len(password) <= 14):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True


# ── Auth Routes ──────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Redirect root to login."""
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip()
        phone    = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm_password", "")

        # ── Validations ──
        if not all([name, email, phone, password, confirm]):
            flash("All fields are required.", "danger")
            return redirect(url_for("signup"))

        if password != confirm:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("signup"))

        if not validate_password(password):
            flash("Password must be 8–14 chars with uppercase, lowercase, number & special character.", "danger")
            return redirect(url_for("signup"))

        if User.query.filter_by(email=email).first():
            flash("Email already registered. Please login.", "warning")
            return redirect(url_for("login"))

        # ── Save user ──
        new_user = User(
            name=name,
            email=email,
            phone=phone,
            password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not all([email, password]):
            flash("Email and password are required.", "danger")
            return redirect(url_for("login"))

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid email or password.", "danger")
            return redirect(url_for("login"))

        # ── Set session ──
        session["user_id"] = user.id
        session["user_name"] = user.name

        flash(f"Welcome back, {user.name}!", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


# ── Dashboard ────────────────────────────────────────────────────────────────

@app.route("/dashboard")
@login_required
def dashboard():
    current_user = User.query.get(session["user_id"])
    all_users    = User.query.all()
    return render_template("dashboard.html", user=current_user, users=all_users)


# ── Student CRUD ─────────────────────────────────────────────────────────────

@app.route("/students")
@login_required
def students():
    all_students = Student.query.all()
    return render_template("students.html", students=all_students)


@app.route("/add_student", methods=["GET", "POST"])
@login_required
def add_student():
    if request.method == "POST":
        name   = request.form.get("name", "").strip()
        email  = request.form.get("email", "").strip()
        course = request.form.get("course", "").strip()
        phone  = request.form.get("phone", "").strip()

        if not all([name, email, course, phone]):
            flash("All fields are required.", "danger")
            return redirect(url_for("add_student"))

        if Student.query.filter_by(email=email).first():
            flash("A student with this email already exists.", "warning")
            return redirect(url_for("add_student"))

        new_student = Student(name=name, email=email, course=course, phone=phone)
        db.session.add(new_student)
        db.session.commit()

        flash(f"Student '{name}' added successfully!", "success")
        return redirect(url_for("students"))

    return render_template("add_student.html")


@app.route("/edit_student/<int:student_id>", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == "POST":
        name   = request.form.get("name", "").strip()
        email  = request.form.get("email", "").strip()
        course = request.form.get("course", "").strip()
        phone  = request.form.get("phone", "").strip()

        if not all([name, email, course, phone]):
            flash("All fields are required.", "danger")
            return redirect(url_for("edit_student", student_id=student_id))

        # Check email conflict with another student
        existing = Student.query.filter_by(email=email).first()
        if existing and existing.id != student_id:
            flash("Another student with this email already exists.", "warning")
            return redirect(url_for("edit_student", student_id=student_id))

        student.name   = name
        student.email  = email
        student.course = course
        student.phone  = phone
        db.session.commit()

        flash(f"Student '{name}' updated successfully!", "success")
        return redirect(url_for("students"))

    return render_template("edit_student.html", student=student)


@app.route("/delete_student/<int:student_id>")
@login_required
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    name = student.name
    db.session.delete(student)
    db.session.commit()
    flash(f"Student '{name}' deleted successfully!", "success")
    return redirect(url_for("students"))


# ── Run ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
