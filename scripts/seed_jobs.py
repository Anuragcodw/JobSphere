
import sys, os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)   

from app import create_app
from app.extensions import db
from app.models.job import Job

app = create_app()

jobs_to_create = [

    {
        "title": "Python Developer",
        "company_name": "Acme Software",
        "required_skills": ["python", "django", "rest", "sql", "git"],
        "min_experience": 1.0,
    },

    {
        "title": "Frontend Developer",
        "company_name": "Pixel Labs",
        "required_skills": ["javascript", "react", "html", "css", "redux"],
        "min_experience": 0.5,
    },

    {
        "title": "Full-Stack Developer",
        "company_name": "StackTech Pvt Ltd",
        "required_skills": ["python", "flask", "react", "sql", "docker"],
        "min_experience": 1.5,
    },

    {
        "title": "Machine Learning Engineer",
        "company_name": "AI Innovations",
        "required_skills": ["python", "tensorflow", "pytorch", "ml", "numpy", "pandas"],
        "min_experience": 1.0,
    },

    {
        "title": "Data Analyst",
        "company_name": "Insight Analytics",
        "required_skills": ["python", "excel", "sql", "powerbi", "data analysis"],
        "min_experience": 0.5,
    },

    {
        "title": "Backend Developer (Node.js)",
        "company_name": "CloudByte",
        "required_skills": ["node", "express", "mongodb", "rest", "git"],
        "min_experience": 1.0,
    },

    {
        "title": "UI/UX Designer",
        "company_name": "Creative Studios",
        "required_skills": ["figma", "ui design", "ux research", "wireframe"],
        "min_experience": 0.5,
    },

    {
        "title": "DevOps Engineer",
        "company_name": "DevOps Hub",
        "required_skills": ["aws", "docker", "kubernetes", "linux", "git"],
        "min_experience": 1.0,
    },

    {
        "title": "Cybersecurity Analyst",
        "company_name": "SecureNet",
        "required_skills": ["network security", "linux", "firewalls", "python"],
        "min_experience": 1.0,
    },

    {
        "title": "Cloud Engineer",
        "company_name": "SkyCloud Services",
        "required_skills": ["aws", "gcp", "azure", "docker", "terraform"],
        "min_experience": 1.5,
    },
]

with app.app_context():
    count = 0
    for job_data in jobs_to_create:
        job = Job(
            title=job_data["title"],
            company_name=job_data["company_name"],
            required_skills=json.dumps(job_data["required_skills"]),
            min_experience=job_data["min_experience"],
        )
        db.session.add(job)
        count += 1

    db.session.commit()
    print(f"🌟 Successfully inserted {count} jobs into database!")
