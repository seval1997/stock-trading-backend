from flask import Flask
from src.api.auth_api import auth_bp
from src.api.users_api import users_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)


@app.route("/api/health")
def health():
    return {"status": "ok", "message": "Backend is alive"}


if __name__ == "__main__":
    app.run(debug=True)
