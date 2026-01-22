from app import create_app
from admin import admin_bp
import os
from flask import send_from_directory

app = create_app()
app.register_blueprint(admin_bp)

# Google verification file route
@app.route("/googlebe5a9285b24fdce8.html")
def google_verify():
    return send_from_directory("app/static", "googlebe5a9285b24fdce8.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
