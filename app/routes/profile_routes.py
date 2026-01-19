import os
import json
import time

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    current_app,
)

from werkzeug.utils import secure_filename

from app.extensions import db
from app.models.user import User

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")

ALLOWED_EXT = {"pdf"}


# ================= FILE CHECK =================
def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


# ================= CURRENT USER =================
def get_current_user():
    """
    Return logged-in User or None
    """
    user_id = session.get("user_id")
    if not user_id:
        return None

    try:
        return User.query.get(user_id)
    except Exception:
        current_app.logger.exception("Error fetching current user")
        return None


# ================= PROFILE HOME =================
@profile_bp.route("/", methods=["GET"])
def profile_home():
    user = get_current_user()

    if not user:
        flash("Please login to view your profile.", "error")
        return redirect(url_for("auth.login"))

    # 🔥 ADMIN KO ALAG PROFILE PAGE
    if getattr(user, "role", None) == "admin" or getattr(user, "is_admin", False):
        return render_template(
            "admin/profile.html",
            user=user
        )

    # 🧑 NORMAL USER PROFILE
    completion = 0
    if hasattr(user, "profile_completion"):
        try:
            completion = user.profile_completion()
        except Exception:
            completion = 0

    return render_template(
        "profile/profile.html",
        user=user,
        profile_completion=completion,
    )


# ================= EDIT PROFILE =================
@profile_bp.route("/edit", methods=["GET", "POST"])
def edit_profile():
    user = get_current_user()
    if not user:
        flash("Please login to edit your profile.", "error")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        try:
            user.full_name = request.form.get("full_name") or user.full_name
            user.phone = request.form.get("phone") or None
            user.location = request.form.get("location") or None
            user.bio = request.form.get("bio") or None
            user.linkedin_url = request.form.get("linkedin_url") or None
            user.github_url = request.form.get("github_url") or None
            user.experience_years = request.form.get("experience_years") or None
            user.education_text = request.form.get("education_text") or None

            db.session.commit()
            flash("Profile updated successfully.", "success")
            return redirect(url_for("profile.profile_home"))

        except Exception:
            db.session.rollback()
            current_app.logger.exception("Profile update failed")
            flash("Failed to update profile.", "error")

    return render_template("profile/edit_profile.html", user=user)


# ================= UPLOAD RESUME =================
@profile_bp.route("/upload_resume", methods=["GET", "POST"])
def upload_resume():
    user = get_current_user()
    if not user:
        flash("Session expired. Please login again.", "error")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        file = request.files.get("resume")

        if not file or file.filename == "":
            flash("Please choose a PDF resume.", "error")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Only PDF files allowed.", "error")
            return redirect(request.url)

        filename = secure_filename(file.filename)

        upload_dir = os.path.join(
            current_app.root_path, "static", "uploads", "resumes"
        )
        os.makedirs(upload_dir, exist_ok=True)

        unique_name = f"user{user.id}_{int(time.time())}_{filename}"
        save_path = os.path.join(upload_dir, unique_name)

        try:
            file.save(save_path)
        except Exception:
            flash("Failed to save resume.", "error")
            return redirect(request.url)

        # ===== Resume Parsing =====
        try:
            from app.services.ocr_resume_parser import parse_resume_file
            parsed = parse_resume_file(save_path)
        except Exception:
            parsed = {
                "skills": [],
                "experience_years": None,
                "education": "",
            }

        try:
            user.resume_filename = unique_name
            user.parsed_skills = json.dumps(parsed.get("skills", []))
            user.experience_years = parsed.get("experience_years")
            user.education_text = parsed.get("education", "")

            db.session.commit()
        except Exception:
            db.session.rollback()
            flash("Profile update failed after upload.", "error")
            return redirect(request.url)

        flash("Resume uploaded & profile updated.", "success")
        return redirect(url_for("profile.profile_home"))

    return render_template("profile/upload_resume.html", user=user)
