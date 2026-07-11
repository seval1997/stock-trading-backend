from flask import Blueprint, request, jsonify
from backend.src.services.auth_service import (
    login_user,
    logout_user,
    refresh_token
)

# Create Blueprint for auth routes
auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

# -------------------------------
# POST /api/auth/login
# -------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    result = login_user(username, password)
    if result.get("error"):
        return jsonify(result), 401

    return jsonify(result), 200


# -------------------------------
# POST /api/auth/logout
# -------------------------------
@auth_bp.route("/logout", methods=["POST"])
def logout():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Authorization token required"}), 400

    result = logout_user(token)
    return jsonify(result), 200


# -------------------------------
# POST /api/auth/refresh
# -------------------------------
@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Authorization token required"}), 400

    result = refresh_token(token)
    if result.get("error"):
        return jsonify(result), 401

    return jsonify(result), 200
