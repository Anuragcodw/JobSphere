from urllib.parse import urlparse, urljoin
from flask_login import login_user, logout_user

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)
import os

from app.extensions import db
from app.models.user import User


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def is_safe_url(target):
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return (
        redirect_url.scheme in ("http", "https")
        and host_url.netloc == redirect_url.netloc
    )


# ================= REGISTER =================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not full_name or not email or not password:
            flash("All fields are required.", "error")
            return redirect(url_for("auth.register"))

        if password != confirm:
            flash("Passwords do not match.", "error")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "error")
            return redirect(url_for("auth.login"))

        user = User(full_name=full_name, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Account created. Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


# ================= LOGIN (🔥 FIXED) =================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Invalid email or password.", "error")
            return redirect(url_for("auth.login"))

        # -------- ADMIN AUTO DETECT (SAFE) --------
        OWNER_EMAIL = os.getenv("OWNER_EMAIL")
        if OWNER_EMAIL and user.email == OWNER_EMAIL:
            user.is_admin = True
            user.role = "admin"
            user.is_active = True
            db.session.commit()
        # ------------------------------------------

        # 🔥 Flask-Login
        login_user(user)

        # 🔥 Legacy session (VERY IMPORTANT – do NOT remove)
        session["user_id"] = user.id
        session["user_name"] = user.full_name
        session["is_admin"] = user.is_admin
        session.permanent = True

        flash("Logged in successfully.", "success")

        next_url = request.args.get("next")
        if next_url and is_safe_url(next_url):
            return redirect(next_url)

        # -------- ROLE BASED REDIRECT --------
        if user.is_admin:
            return redirect(url_for("admin.dashboard"))

        return redirect(url_for("profile.profile_home"))

    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    logout_user()        # flask-login
    session.clear()      # legacy session
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
