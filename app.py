from app import create_app
from admin import admin_bp
import os

# 🔥 app create
app = create_app()
app.register_blueprint(admin_bp)



# 🔥 run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
