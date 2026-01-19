
import sys, os, glob

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from app import create_app
from app.models.user import User

TEST_EMAIL = "vishusingh2382@gmail.com"

app = create_app()

with app.app_context():
    u = User.query.filter_by(email=TEST_EMAIL).first()
    if not u:
        print("❌ User not found:", TEST_EMAIL)
        raise SystemExit(1)

    print("\n=== USER INFO ===")
    print("ID:", u.id)
    print("Resume filename in DB:", repr(u.resume_filename))

    uploads_dir = os.path.join(app.root_path, "static", "uploads", "resumes")
    print("Uploads dir:", uploads_dir)

    if u.resume_filename:
        path = os.path.join(uploads_dir, u.resume_filename)
    else:
        pattern = os.path.join(uploads_dir, f"user{u.id}_*")
        files = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
        path = files[0] if files else None

    print("Using file:", path)
    if not path or not os.path.exists(path):
        print("❌ Resume file NOT FOUND for this user.")
        raise SystemExit(1)

    from app.services.ocr_resume_parser import parse_resume_file

    parsed = parse_resume_file(path)

    print("\n=== PARSER OUTPUT ===")
    print("Skills:", parsed.get("skills"))
    print("Experience:", parsed.get("experience_years"))
    print("Education:", parsed.get("education"))
