import datetime
import os
from dotenv import load_dotenv
from src.repositories.user_repo import UserRepository
from passlib.hash import pbkdf2_sha256
import jwt

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")


def _build_token(user_id: str) -> str:
    """Generate JWT token with expiry."""
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


# Mock user validation (replace with DB lookup)
def login_user(username, password):
    user = UserRepository.get_by_username(username)
    if not user:
        return {"error": "Invalid credentials"}

    # Verify password against stored hash
    if not pbkdf2_sha256.verify(password, user["password"]):
        return {"error": "Invalid credentials"}

    # Build JWT token
    token = _build_token(str(user["_id"]))
    return {"token": token, "message": "Login successful"}


def logout_user(token):
    # In real implementation, blacklist token or manage session store
    return {"message": "Logout successful"}


def refresh_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        new_token = _build_token(payload["user_id"])
        return {"token": new_token, "message": "Token refreshed"}
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
