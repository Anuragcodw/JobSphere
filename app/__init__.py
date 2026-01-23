# app/__init__.py
import pymysql
pymysql.install_as_MySQLdb()   # safe even if not using PyMySQL

from flask import Flask, session, send_from_directory
from config import Config
from app.extensions import db, login_manager   # ✅ STEP-2 ADD
from app.models.user import User               # ✅ STEP-2 ADD


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ---- Initialize extensions ----
    db.init_app(app)

    # ================= STEP-2: Flask-Login INIT =================
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    # ============================================================

    # ---- Register blueprints ----
    from app.routes.main_routes import main_bp
    from app.routes.jobs_routes import jobs_bp
    from app.routes.auth_routes import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(auth_bp)

    # ---- Optional blueprints ----
    try:
        from app.routes.companies_routes import companies_bp
        app.register_blueprint(companies_bp)
    except Exception:
        pass

    try:
        from app.routes.profile_routes import profile_bp
        app.register_blueprint(profile_bp)
    except Exception:
        pass

    # ---- Context processor: inject current_user + is_admin ----
    @app.context_processor
    def inject_current_user():
        """
        Makes `current_user` and `is_admin` available in all templates.
        """
        user = None
        is_admin = False

        try:
            user_id = session.get("user_id")
            if user_id:
                user = User.query.get(user_id)
                if user:
                    is_admin = bool(user.is_admin)
        except Exception:
            user = None
            is_admin = False

        return dict(
            current_user=user,
            is_admin=is_admin
        )

    # ---- Debug DB URI (masked) ----
    try:
        uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
        if uri:
            display_uri = uri
            if "://" in uri and "@" in uri:
                scheme, rest = uri.split("://", 1)
                if "@" in rest:
                    _, host = rest.split("@", 1)
                    display_uri = f"{scheme}://***@{host}"
            print("SQLALCHEMY_DATABASE_URI:", display_uri)
    except Exception:
        pass

    # ---- Create DB tables ----
    with app.app_context():
        try:
            from app.models.application import Application
            db.create_all()
            print("DB create_all() ran successfully.")
        except Exception as e:
            print("DB create_all() error:", repr(e))

    # ---- Google Search Console Verification ----
    # app/__init__.py ke end me, return app se pehle

    @app.route("/googlebe5a9285b24fdce8.html")
    def google_verify():
        return send_from_directory(app.static_folder, "googlebe5a9285b24fdce8.html")

    @app.route("/sitemap.xml")
    def sitemap():
        return send_from_directory(app.static_folder, "sitemap.xml")

    return app
