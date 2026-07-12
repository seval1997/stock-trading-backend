from functools import wraps
from flask import request, jsonify
import jwt

SECRET_KEY = "this_is_a_long_random_secret_key_for_testing_123456"  # move to config/env


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Authorization token required"}), 400

        token = auth_header.replace("Bearer ", "")
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # Optionally attach user_id to kwargs
            kwargs["current_user_id"] = data["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated
