from functools import wraps
from flask import request, jsonify


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        # For now, just accept any non-empty token
        # Later, replace with JWT verification
        return f(*args, **kwargs)

    return decorated
