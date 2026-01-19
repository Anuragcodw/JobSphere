from flask import Blueprint, render_template
from flask import Blueprint, render_template, request
from flask import render_template, redirect, url_for
from flask_login import current_user

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    if current_user.is_authenticated and current_user.role == "admin":
        return redirect(url_for("admin.dashboard"))

    return render_template("home.html")


@main_bp.route("/companies", methods=["GET"])
def companies():
    
    name = request.args.get("name", "").strip()

    google_url = None
    jobs_url = None

    if name:
        from urllib.parse import quote_plus

        query = f"{name} company official website"
        jobs_query = f"{name} jobs"

        google_url = "https://www.google.com/search?q=" + quote_plus(query)
        jobs_url = "https://www.google.com/search?q=" + quote_plus(jobs_query)

    return render_template(
        "companies.html",
        name=name,
        google_url=google_url,
        jobs_url=jobs_url,
    )
