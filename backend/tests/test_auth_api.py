import pytest
from flask import Flask
from src.api.auth_api import auth_bp
from src.api.users_api import users_bp


@pytest.fixture
def client(monkeypatch):
    app = Flask(__name__)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.config["TESTING"] = True
    client = app.test_client()

    class DummyUserRepo:
        store = {}

        @staticmethod
        def create(user_obj):
            user_obj["_id"] = "fakeid123"
            # hash password before storing, just like signup_user does
            DummyUserRepo.store[user_obj["username"]] = user_obj
            return user_obj

        @staticmethod
        def get_by_username(username):
            return DummyUserRepo.store.get(username)

        @staticmethod
        def get_by_id(user_id):
            # not used in auth, but needed for users_api
            return DummyUserRepo.store.get("demo")

        @staticmethod
        def update(user_id, update_data):
            return None

        @staticmethod
        def delete(user_id):
            return True

    monkeypatch.setattr("src.api.users_api.UserRepository", DummyUserRepo)
    monkeypatch.setattr("src.api.auth_api.UserRepository", DummyUserRepo)

    return client


def test_login_success(client):
    payload = {
        "username": "demo",
        "email": "demo@example.com",
        "password": "password123",
        "full_name": "Demo User",
        "phone_number": "1234567890",
        "dob": "1990-01-01",
        "pan_number": "ABCDE1234F",
    }
    response = client.post("/api/users/sign-up", json=payload)
    response = client.post(
        "/api/auth/login", json={"username": "demo", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Login successful"
    assert "token" in data


def test_login_failure(client):
    response = client.post(
        "/api/auth/login", json={"username": "wrong", "password": "badpass"}
    )
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data


def test_login_missing_fields(client):
    response = client.post("/api/auth/login", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Username and password required"


def test_logout_success(client):
    headers = {"Authorization": "Bearer faketoken"}
    response = client.post("/api/auth/logout", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Logout successful"


def test_logout_missing_token(client):
    response = client.post("/api/auth/logout")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Authorization token required"


def test_refresh_missing_token(client):
    response = client.post("/api/auth/refresh")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Authorization token required"


def test_refresh_success(client):
    payload = {
        "username": "demo2",
        "email": "demo2@example.com",
        "password": "password123",
        "full_name": "Demo User 2",
        "phone_number": "1234567890",
        "dob": "1990-01-01",
        "pan_number": "ABCDE1234F",
    }
    client.post("/api/users/sign-up", json=payload)

    login_resp = client.post(
        "/api/auth/login", json={"username": "demo2", "password": "password123"}
    )
    assert login_resp.status_code == 200
    token = login_resp.get_json()["token"]

    headers = {"Authorization": f"Bearer {token}"}
    refresh_resp = client.post("/api/auth/refresh", headers=headers)
    assert refresh_resp.status_code == 200
    data = refresh_resp.get_json()
    assert "token" in data
