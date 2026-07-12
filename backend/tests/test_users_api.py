import pytest
from flask import Flask
from src.api.users_api import users_bp


@pytest.fixture
def client(monkeypatch):
    # Create a Flask app and register the blueprint
    app = Flask(__name__)
    app.register_blueprint(users_bp)
    client = app.test_client()

    # Patch UserRepository.create to avoid real DB
    class DummyUserRepo:
        @staticmethod
        def create(user_obj):
            # Simulate DB insert by returning user_obj with fake _id
            user_obj["_id"] = "fakeid123"
            return user_obj

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
        "aadhaar_number": "123412341234",
        "address": {"city": "Ahmedabad", "state": "Gujarat"},
        "bank_details": {"account_number": "123456789012", "ifsc_code": "HDFC0001234"},
    }
    response = client.post("/api/users/sign-up", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "User registered successfully"
    assert data["user_id"] == "fakeid123"


def test_signup_missing_field(client):
    payload = {
        "username": "seval123",
        "email": "seval@example.com",
        # password missing
        "full_name": "Seval Patel",
        "phone_number": "+91-9876543210",
        "dob": "1990-05-15",
        "pan_number": "ABCDE1234F",
    }
    response = client.post("/api/users/sign-up", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "password is required" in data["error"]
