from datetime import datetime
from app.extensions import db


class JobReview(db.Model):
    __tablename__ = "job_reviews"

    id = db.Column(db.Integer, primary_key=True)

    # जिस job par review diya gaya
    job_id = db.Column(
        db.Integer,
        db.ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False
    )

    # reviewer ka naam (user.full_name se)
    user_name = db.Column(db.String(120), nullable=False)

    # 1 से 5 तक rating
    rating = db.Column(db.Integer, nullable=False, default=5)

    # user ka comment
    comment = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<JobReview job_id={self.job_id} rating={self.rating}>"
