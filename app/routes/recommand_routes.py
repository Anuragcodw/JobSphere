
from app.services.job_matcher import rank_jobs_for_user

@profile_bp.route("/recommendations", methods=["GET"])
def recommendations():
    
    if "user_id" not in session:
        return redirect(url_for("auth.login", next=url_for("profile.recommendations")))

    user = get_current_user()
    if not user:
        flash("Please login", "error")
        return redirect(url_for("auth.login"))

    from app.models.job import Job
    jobs = Job.query.all()   

    ranked = rank_jobs_for_user(user, jobs, top_n=50)

    return render_template("profile/recommendations.html", ranked=ranked, user=user)
