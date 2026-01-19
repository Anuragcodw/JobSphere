from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import json


class User(db.Model, UserMixin):
    __tablename__ = "user"   # ✅ KEEP OLD TABLE

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Admin flags
    is_admin = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(20), default="user")

    is_active = db.Column(db.Boolean, default=True)

    # ✅ relationship (correct place)
    applications = db.relationship(
        "Application",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # Search tracking
    last_search_q = db.Column(db.String(255))
    last_search_location = db.Column(db.String(255))

    # Profile
    phone = db.Column(db.String(20))
    location = db.Column(db.String(120))
    bio = db.Column(db.Text)

    avatar = db.Column(db.String(255))
    linkedin_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))

    resume_filename = db.Column(db.String(255))
    parsed_skills = db.Column(db.Text)
    experience_years = db.Column(db.Float)
    education_text = db.Column(db.Text)

    # ================= PASSWORD =================
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # ================= SKILLS =================
    def get_skills_list(self):
        if not self.parsed_skills:
            return []
        try:
            return json.loads(self.parsed_skills)
        except Exception:
            return []

    # ================= 🔥 FIXED METHOD =================
    def profile_completion(self):
        """
        Returns profile completion percentage (0–100)
        """
        score = 0

        score += 10  # name
        score += 10  # email

        if self.resume_filename:
            score += 20
        if self.parsed_skills:
            score += 20
        if self.experience_years:
            score += 15
        if self.education_text:
            score += 15
        if self.phone:
            score += 5
        if self.location:
            score += 5
        if self.bio:
            score += 5
        if self.linkedin_url or self.github_url:
            score += 5

        return min(score, 100)
    # ==================================================

    def __repr__(self):
        return f"<User {self.email} role={self.role}>"
