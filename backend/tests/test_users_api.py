import pytest
from flask import Flask
from src.api.users_api import users_bp
from src.middleware.auth_middleware import make_token


@pytest.fixture
def client(monkeypatch):
    # Create a Flask app and register the blueprint
    app = Flask(__name__)
    app.register_blueprint(users_bp)
    client = app.test_client()

    # Dummy UserRepository for testing
    class DummyUserRepo:
        store = {}

        @staticmethod
        def create(user_obj):
            user_obj["_id"] = "fakeid123"
            DummyUserRepo.store[user_obj["_id"]] = user_obj
            return user_obj

        @staticmethod
        def get_by_id(user_id):
            return DummyUserRepo.store.get(user_id)

        @staticmethod
        def update(user_id, update_data):
            if user_id not in DummyUserRepo.store:
                return None
            DummyUserRepo.store[user_id].update(update_data)
            return DummyUserRepo.store[user_id]

        @staticmethod
        def delete(user_id):
            return DummyUserRepo.store.pop(user_id, None) is not None

    monkeypatch.setattr("src.api.users_api.UserRepository", DummyUserRepo)
    return client


def test_signup_success(client):
    payload = {
        "username": "seval123",
        "email": "seval@example.com",
        "password": "StrongPassword!123",
        "full_name": "Seval Patel",
        "phone_number": "+91-9876543210",
        "dob": "1990-05-15",
        "pan_number": "ABCDE1234F",
    }
    response = client.post("/api/users/sign-up", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "User registered successfully"
    assert data["user_id"] == "fakeid123"


def test_get_user(client):
    # First create user
    payload = {
        "username": "getme",
        "email": "getme@example.com",
        "password": "pw",
        "full_name": "Get Me",
        "phone_number": "123",
        "dob": "2000-01-01",
        "pan_number": "PAN123",
    }
    client.post("/api/users/sign-up", json=payload)
    token = make_token("fakeid123")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/users/fakeid123", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == "getme"


def test_update_user(client):
    payload = {
        "username": "oldname",
        "email": "old@example.com",
        "password": "pw",
        "full_name": "Old Name",
        "phone_number": "123",
        "dob": "2000-01-01",
        "pan_number": "PAN123",
    }
    client.post("/api/users/sign-up", json=payload)
    token = make_token("fakeid123")
    print("Token for update test:", token)
    headers = {"Authorization": f"Bearer {token}"}
    # Update username
    response = client.put(
        "/api/users/fakeid123", json={"username": "newname"}, headers=headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == "newname"
    # Verify with GET
    response = client.get("/api/users/fakeid123", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == "newname"


def test_delete_user(client):
    payload = {
        "username": "todelete",
        "email": "del@example.com",
        "password": "pw",
        "full_name": "Delete Me",
        "phone_number": "123",
        "dob": "2000-01-01",
        "pan_number": "PAN123",
    }
    client.post("/api/users/sign-up", json=payload)
    token = make_token("fakeid123")
    headers = {"Authorization": f"Bearer {token}"}
    # Delete user
    response = client.delete("/api/users/fakeid123", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User deleted"
    # Verify with GET → should be 404 now
    response = client.get("/api/users/fakeid123", headers=headers)
    assert response.status_code == 404
