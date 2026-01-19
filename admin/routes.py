from flask import (
    render_template,
    redirect,
    url_for,
    abort,
    send_from_directory,
    current_app,
    request
)
from flask_login import login_required
from app.models.user import User
from app.models.job import Job, JobReview   # 🔥 JobReview added
from app.extensions import db
from . import admin_bp
from utils.decorators import admin_required
import os
from sqlalchemy import func


# ================= ADMIN DASHBOARD =================
@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    total_jobs = Job.query.count()

    # 🔥 Reviews stats
    total_reviews = JobReview.query.count()
    avg_rating = db.session.query(func.avg(JobReview.rating)).scalar() or 0
    avg_rating = round(float(avg_rating), 2)

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        active_users=active_users,
        total_jobs=total_jobs,
        total_reviews=total_reviews,
        avg_rating=avg_rating,
    )


# ================= USER LIST (PAGINATED) =================
@admin_bp.route("/users")
@login_required
@admin_required
def users():
    page = request.args.get("page", 1, type=int)
    per_page = 10

    pagination = (
        User.query
        .filter(User.role != "admin")
        .order_by(User.id.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return render_template(
        "admin/users.html",
        users=pagination.items,
        pagination=pagination
    )


# ================= ACTIVATE / DEACTIVATE USER =================
@admin_bp.route("/users/toggle/<int:user_id>")
@login_required
@admin_required
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)

    if user.role == "admin":
        abort(403)

    user.is_active = not user.is_active
    db.session.commit()

    return redirect(url_for("admin.users"))


# ================= VIEW USER RESUME =================
@admin_bp.route("/users/resume/<int:user_id>")
@login_required
@admin_required
def view_resume(user_id):
    user = User.query.get_or_404(user_id)

    if not user.resume_filename:
        return redirect(url_for("admin.users"))

    resume_dir = os.path.join(
        current_app.root_path,
        "static",
        "uploads",
        "resumes"
    )

    return send_from_directory(
        resume_dir,
        user.resume_filename,
        as_attachment=False
    )


# ================= JOB LIST (WITH LOCATION FILTER) =================
@admin_bp.route("/jobs")
@login_required
@admin_required
def jobs():
    page = request.args.get("page", 1, type=int)
    per_page = 10

    location = request.args.get("location", "").strip()
    query = Job.query

    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))

    pagination = query.order_by(Job.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template(
        "admin/jobs.html",
        jobs=pagination.items,
        pagination=pagination,
        selected_location=location
    )


# ================= APPROVE / REJECT JOB =================
@admin_bp.route("/jobs/toggle/<int:job_id>")
@login_required
@admin_required
def toggle_job(job_id):
    job = Job.query.get_or_404(job_id)

    if not hasattr(job, "is_approved"):
        abort(500, description="is_approved column missing in Job model")

    job.is_approved = not bool(job.is_approved)
    db.session.commit()

    return redirect(
        url_for("admin.jobs", location=request.args.get("location"))
    )


# ================= DELETE JOB =================
@admin_bp.route("/jobs/delete/<int:job_id>")
@login_required
@admin_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)

    db.session.delete(job)
    db.session.commit()

    return redirect(
        url_for("admin.jobs", location=request.args.get("location"))
    )


# ================= ANALYTICS =================
@admin_bp.route("/analytics")
@login_required
@admin_required
def analytics():
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()

    total_jobs = Job.query.count()
    approved_jobs = Job.query.filter_by(is_approved=True).count()
    pending_jobs = Job.query.filter_by(is_approved=False).count()

    return render_template(
        "admin/analytics.html",
        total_users=total_users,
        active_users=active_users,
        total_jobs=total_jobs,
        approved_jobs=approved_jobs,
        pending_jobs=pending_jobs,
    )


# ================= REVIEWS (NEW ADMIN PAGE) =================
@admin_bp.route("/reviews")
@login_required
@admin_required
def reviews():
    page = request.args.get("page", 1, type=int)
    per_page = 10

    pagination = (
        JobReview.query
        .order_by(JobReview.created_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    avg_rating = db.session.query(func.avg(JobReview.rating)).scalar() or 0
    avg_rating = round(float(avg_rating), 2)

    return render_template(
        "admin/reviews.html",
        reviews=pagination.items,
        pagination=pagination,
        avg_rating=avg_rating
    )
