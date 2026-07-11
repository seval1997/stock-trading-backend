import os
import jwt
import datetime
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")

# Mock user validation (replace with DB lookup)
def login_user(username, password):
    if username == "demo" and password == "password123":
        token = jwt.encode(
            {"username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            SECRET_KEY,
            algorithm="HS256"
        )
        return {"token": token, "message": "Login successful"}
    return {"error": "Invalid credentials"}

def logout_user(token):
    # In real implementation, blacklist token or manage session store
    return {"message": "Logout successful"}

def refresh_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        new_token = jwt.encode(
            {"username": payload["username"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            SECRET_KEY,
            algorithm="HS256"
        )
        return {"token": new_token, "message": "Token refreshed"}
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
