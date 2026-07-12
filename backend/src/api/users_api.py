from flask import Blueprint, request, jsonify
from src.repositories.user_repo import UserRepository
from passlib.hash import pbkdf2_sha256
from src.middleware.auth_middleware import token_required


users_bp = Blueprint("users", __name__, url_prefix="/api/users")


@users_bp.route("/sign-up", methods=["POST"])
def signup_user():
    data = request.get_json()
    # Required fields
    required_fields = [
        "username",
        "email",
        "password",
        "full_name",
        "phone_number",
        "dob",
        "pan_number",
    ]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400
    # Hash password
    hashed_password = pbkdf2_sha256.hash(data["password"])
    # Build user object
    user_obj = {
        "username": data["username"],
        "email": data["email"],
        "password": hashed_password,
        "full_name": data["full_name"],
        "phone_number": data["phone_number"],
        "dob": data["dob"],
        "pan_number": data["pan_number"],
        "aadhaar_number": data.get("aadhaar_number"),
        "address": data.get("address"),
        "bank_details": data.get("bank_details"),
    }
    # Save to DB
    user = UserRepository.create(user_obj)
    return (
        jsonify(
            {"message": "User registered successfully", "user_id": str(user["_id"])}
        ),
        201,
    )


@users_bp.route("/<user_id>", methods=["GET"])
@token_required
def get_user(user_id):
    user = UserRepository.get_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    # Convert ObjectId to string for JSON
    user["_id"] = str(user["_id"])
    return jsonify(user), 200


@users_bp.route("/<user_id>", methods=["PUT"])
@token_required
def update_user(user_id):
    data = request.get_json()
    user = UserRepository.update(user_id, data)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user["_id"] = str(user["_id"])
    return jsonify(user), 200


@users_bp.route("/<user_id>", methods=["DELETE"])
@token_required
def delete_user(user_id):
    deleted = UserRepository.delete(user_id)
    if not deleted:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted"}), 200
