# backend/tests/test_auth_api.py
import pytest
from flask import Flask
from backend.src.api.auth_api import auth_bp
from backend.src import db

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(auth_bp)
    app.config["TESTING"] = True
    return app.test_client()

@pytest.fixture(scope="module", autouse=True)
def seed_users():
    db.db.users.insert_one({
        "username": "testuser",
        "password": "hashedpassword",
        "email": "test@example.com"
    })
    yield
    db.db.users.delete_many({})

def test_login_success(client):
    response = client.post("/api/auth/login", json={
        "username": "demo",
        "password": "password123"
    })
    data = response.get_json()
    assert response.status_code == 200
    assert "token" in data
    assert data["message"] == "Login successful"

def test_login_failure(client):
    response = client.post("/api/auth/login", json={
        "username": "wrong",
        "password": "badpass"
    })
    data = response.get_json()
    assert response.status_code == 401
    assert "error" in data

def test_login_missing_fields(client):
    response = client.post("/api/auth/login", json={})
    data = response.get_json()
    assert response.status_code == 400
    assert data["error"] == "Username and password required"

def test_logout(client):
    # token is not validated in mock service, any string works
    response = client.post("/api/auth/logout", headers={
        "Authorization": "dummy_token"
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data["message"] == "Logout successful"

def test_logout_missing_token(client):
    response = client.post("/api/auth/logout")
    data = response.get_json()
    assert response.status_code == 400
    assert data["error"] == "Authorization token required"

def test_refresh_success(client):
    # First login to get a valid token
    login_resp = client.post("/api/auth/login", json={
        "username": "demo",
        "password": "password123"
    })
    token = login_resp.get_json()["token"]

    refresh_resp = client.post("/api/auth/refresh", headers={
        "Authorization": token
    })
    data = refresh_resp.get_json()
    assert refresh_resp.status_code == 200
    assert "token" in data
    assert data["message"] == "Token refreshed"

def test_refresh_missing_token(client):
    response = client.post("/api/auth/refresh")
    data = response.get_json()
    assert response.status_code == 400
    assert data["error"] == "Authorization token required"
