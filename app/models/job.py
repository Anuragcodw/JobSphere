from app.extensions import db
import json
from datetime import datetime


class Job(db.Model):
    """
    Simple Job model.
    - required_skills stored as JSON text (list of strings)
    - min_experience in years (float)
    """

    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(255), nullable=True)

    # LOCATION (API se aayegi)
    location = db.Column(db.String(255), nullable=True)

    description = db.Column(db.Text, nullable=True)
    required_skills = db.Column(db.Text, nullable=True)
    min_experience = db.Column(db.Float, nullable=True)

    # ADMIN APPROVAL
    is_approved = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # REVIEWS RELATION
    reviews = db.relationship(
        "JobReview",
        backref="job",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # -----------------------------
    def get_required_skills(self):
        if not self.required_skills:
            return []
        try:
            data = json.loads(self.required_skills)

            if isinstance(data, list):
                return [str(x).strip() for x in data if x is not None]

            if isinstance(data, str):
                return [s.strip() for s in data.split(",") if s.strip()]
        except Exception:
            return []
        return []

    def set_required_skills(self, skills):
        try:
            if isinstance(skills, (list, tuple)):
                self.required_skills = json.dumps(
                    [str(s).strip() for s in skills]
                )
            else:
                self.required_skills = json.dumps(
                    [s.strip() for s in str(skills).split(",") if s.strip()]
                )
        except Exception:
            self.required_skills = json.dumps([])

    def __repr__(self):
        return f"<Job id={self.id} title={self.title!r} company={self.company_name!r}>"


# ================= JOB REVIEW MODEL =================
class JobReview(db.Model):
    __tablename__ = "job_reviews"

    id = db.Column(db.Integer, primary_key=True)

    job_id = db.Column(
        db.Integer,
        db.ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False
    )

    user_name = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=5)  # 1–5 stars
    comment = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<JobReview job_id={self.job_id} rating={self.rating}>"
