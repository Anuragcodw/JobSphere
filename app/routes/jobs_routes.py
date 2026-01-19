from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
)
from functools import wraps

from app.models.application import Application
from app.models.job import Job, JobReview   # 🔥 JobReview import
from app.extensions import db
from app.models.user import User
from app.services.adzuna_service import search_jobs_api

jobs_bp = Blueprint("jobs", __name__, url_prefix="/jobs")

LAST_RESULTS = []


# ================= LOGIN REQUIRED =================
def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login", next=request.url))
        return view_func(*args, **kwargs)
    return wrapped


# ================= SEARCH JOBS =================
@jobs_bp.route("/search")
@login_required
def search_jobs():
    global LAST_RESULTS

    user = User.query.get(session.get("user_id"))

    q = (request.args.get("q") or "").strip()
    location = (request.args.get("location") or "").strip()
    job_type = (request.args.get("job_type") or "").strip()
    min_salary = request.args.get("min_salary", type=int)

    if not location and user and user.location:
        location = user.location

    if user:
        if not q and user.last_search_q:
            q = user.last_search_q
        if not location and user.last_search_location:
            location = user.last_search_location

    LAST_RESULTS = search_jobs_api(
        query=q,
        location=location,
        job_type=job_type,
        min_salary=min_salary,
    )

    for api_job in LAST_RESULTS:
        company_obj = api_job.get("company")
        if isinstance(company_obj, dict):
            company_name = company_obj.get("display_name", "").strip()
        elif isinstance(company_obj, str):
            company_name = company_obj.strip()
        else:
            company_name = ""

        loc_obj = api_job.get("location")
        if isinstance(loc_obj, dict):
            location_name = loc_obj.get("display_name", "").strip()
        elif isinstance(loc_obj, str):
            location_name = loc_obj.strip()
        else:
            location_name = ""

        if not company_name or not location_name:
            continue

        exists = Job.query.filter_by(
            title=api_job.get("title"),
            company_name=company_name,
            location=location_name
        ).first()

        if not exists:
            db.session.add(
                Job(
                    title=api_job.get("title"),
                    company_name=company_name,
                    location=location_name,
                    description=api_job.get("description", "")
                )
            )

    db.session.commit()

    if user:
        user.last_search_q = q
        user.last_search_location = location
        db.session.commit()

    return render_template(
        "jobs/search_results.html",
        jobs=LAST_RESULTS,
        q=q,
        location=location,
        job_type=job_type,
        min_salary=min_salary,
    )


# ================= JOB DETAIL =================
@jobs_bp.route("/<int:job_id>")
@login_required
def job_detail(job_id):
    if job_id < 0 or job_id >= len(LAST_RESULTS):
        return "Job not found", 404

    job = LAST_RESULTS[job_id]

    loc = job.get("location")
    if isinstance(loc, dict):
        display = loc.get("display_name", "").strip()
    elif isinstance(loc, str):
        display = loc.strip()
    else:
        display = ""

    job["location_display"] = display

    company_name = ""
    company_obj = job.get("company")
    if isinstance(company_obj, dict):
        company_name = company_obj.get("display_name", "").strip()
    elif isinstance(company_obj, str):
        company_name = company_obj.strip()

    # 🔥 DB job find karo (for reviews)
    db_job = Job.query.filter_by(
        title=job.get("title"),
        company_name=company_name,
        location=display
    ).first()

    reviews = db_job.reviews if db_job else []

    return render_template(
        "jobs/job_detail.html",
        job=job,
        job_id=job_id,
        reviews=reviews,
        db_job=db_job,
    )


# ================= ADD REVIEW =================
@jobs_bp.route("/<int:job_id>/review", methods=["POST"])
@login_required
def add_review(job_id):
    user = User.query.get(session.get("user_id"))
    if not user:
        return redirect(url_for("auth.login"))

    try:
        rating = int(request.form.get("rating", 0))
    except ValueError:
        rating = 0

    comment = request.form.get("comment", "").strip()

    if job_id < 0 or job_id >= len(LAST_RESULTS):
        return "Job not found", 404

    job = LAST_RESULTS[job_id]

    loc = job.get("location")
    if isinstance(loc, dict):
        display = loc.get("display_name", "").strip()
    elif isinstance(loc, str):
        display = loc.strip()
    else:
        display = ""

    company_name = ""
    company_obj = job.get("company")
    if isinstance(company_obj, dict):
        company_name = company_obj.get("display_name", "").strip()
    elif isinstance(company_obj, str):
        company_name = company_obj.strip()

    db_job = Job.query.filter_by(
        title=job.get("title"),
        company_name=company_name,
        location=display
    ).first()

    if not db_job:
        return redirect(url_for("jobs.job_detail", job_id=job_id))

    review = JobReview(
        job_id=db_job.id,
        user_name=user.full_name,
        rating=rating,
        comment=comment,
    )

    db.session.add(review)
    db.session.commit()

    return redirect(url_for("jobs.job_detail", job_id=job_id))


# ================= APPLY JOB =================
@jobs_bp.route("/<int:job_id>/apply", methods=["GET", "POST"])
@login_required
def apply_job(job_id):
    global LAST_RESULTS

    if job_id < 0 or job_id >= len(LAST_RESULTS):
        return "Job not found", 404

    job = LAST_RESULTS[job_id]

    user_id = session.get("user_id")
    user = User.query.get(user_id)

    if not user:
        return redirect(url_for("auth.login"))

    default_email = user.email

    if request.method == "POST":
        email_used = request.form.get("email", "").strip() or default_email

        company_obj = job.get("company")
        company = (
            company_obj.get("display_name", "").strip()
            if isinstance(company_obj, dict)
            else str(company_obj or "").strip()
        )

        location_obj = job.get("location")
        location = (
            location_obj.get("display_name", "").strip()
            if isinstance(location_obj, dict)
            else str(location_obj or "").strip()
        )

        application = Application(
            user_id=user.id,
            job_title=job.get("title", ""),
            company=company,
            location=location,
            adzuna_url=job.get("redirect_url", ""),
            email_used=email_used,
        )

        db.session.add(application)
        db.session.commit()

        return redirect(url_for("jobs.job_detail", job_id=job_id))

    return render_template(
        "jobs/apply_confirm.html",
        job=job,
        default_email=default_email,
        job_id=job_id,
    )
