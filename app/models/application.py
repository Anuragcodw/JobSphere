from datetime import datetime
from app.extensions import db

class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    # 🔧 FIX: Proper ForeignKey
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    job_title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255))
    location = db.Column(db.String(255))
    adzuna_url = db.Column(db.String(500))
    email_used = db.Column(db.String(255))

    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Application {self.job_title} by user {self.user_id}>"
