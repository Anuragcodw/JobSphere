from app import create_app
from admin import admin_bp
import os

# 🔥 app create
app = create_app()
app.register_blueprint(admin_bp)

# 🔥 TEMPORARY DB RESET (STEP-1 FIX)
# ⚠️ Deploy ke baad REMOVE karna hai
with app.app_context():
    try:
        from app.extensions import db
        from app.models.user import User

        User.query.delete()
        db.session.commit()
        print("✅ User table cleared successfully")

    except Exception as e:
        print("❌ DB reset skipped:", e)

# 🔥 run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
