import os
from dotenv import load_dotenv

# Load environment variables automatically
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret Key
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-this")

    # Adzuna API Credentials
    ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
    ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    if not SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "local_job_portal.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Debug (Optional – remove later)
print("DEBUG: APP_ID =", Config.ADZUNA_APP_ID)
print("DEBUG: DATABASE =", Config.SQLALCHEMY_DATABASE_URI)
