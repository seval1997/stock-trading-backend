import datetime
import os

import jwt
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")


def _build_token(username):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    return jwt.encode(
        {"username": username, "exp": expiration},
        SECRET_KEY,
        algorithm="HS256",
    )


# Mock user validation (replace with DB lookup)
def login_user(username, password):
    if username == "demo" and password == "password123":
        token = _build_token(username)
        return {"token": token, "message": "Login successful"}
    return {"error": "Invalid credentials"}


def logout_user(token):
    # In real implementation, blacklist token or manage session store
    return {"message": "Logout successful"}


def refresh_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        new_token = _build_token(payload["username"])
        return {"token": new_token, "message": "Token refreshed"}
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
