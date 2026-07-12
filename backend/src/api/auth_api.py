from flask import Blueprint, request, jsonify
from passlib.hash import pbkdf2_sha256
import jwt
import datetime
from src.repositories.user_repo import UserRepository

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

SECRET_KEY = "this_is_a_long_random_secret_key_for_testing_123456"  # move to config/env


def _build_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    user = UserRepository.get_by_username(username)
    if not user or not pbkdf2_sha256.verify(password, user["password"]):
        return jsonify({"error": "Invalid username or password"}), 401

    token = _build_token(str(user["_id"]))
    return jsonify({"message": "Login successful", "token": token}), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Authorization token required"}), 400
    # In stateless JWT, logout is client‑side (just discard token).
    return jsonify({"message": "Logout successful"}), 200


@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Authorization token required"}), 400

    token = auth_header.replace("Bearer ", "")
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        new_token = _build_token(data["user_id"])
        return jsonify({"token": new_token}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
