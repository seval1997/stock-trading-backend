import pytest
import mongomock
from src.repositories.user_repo import UserRepository


@pytest.fixture(autouse=True)
def mock_db(monkeypatch):
    # Create a fake MongoDB collection
    mock_client = mongomock.MongoClient()
    mock_db = mock_client["testdb"]
    UserRepository.collection = mock_db["users"]
    yield


def test_create_user():
    user_data = {
        "username": "seval123",
        "email": "seval@example.com",
        "password": "hashed_pw",
        "full_name": "Seval Patel",
    }
    user = UserRepository.create(user_data)
    assert "_id" in user
    assert user["username"] == "seval123"


def test_get_by_id():
    user_data = {"username": "testuser", "email": "test@example.com"}
    inserted = UserRepository.create(user_data)
    fetched = UserRepository.get_by_id(str(inserted["_id"]))
    assert fetched is not None
    assert fetched["email"] == "test@example.com"


def test_get_by_email():
    UserRepository.create({"username": "abc", "email": "abc@example.com"})
    user = UserRepository.get_by_email("abc@example.com")
    assert user is not None
    assert user["username"] == "abc"


def test_get_by_username():
    UserRepository.create({"username": "xyz", "email": "xyz@example.com"})
    user = UserRepository.get_by_username("xyz")
    assert user is not None
    assert user["email"] == "xyz@example.com"


def test_update_user():
    user = UserRepository.create({"username": "oldname", "email": "old@example.com"})
    updated = UserRepository.update(str(user["_id"]), {"username": "newname"})
    assert updated["username"] == "newname"


def test_delete_user():
    user = UserRepository.create({"username": "todelete", "email": "del@example.com"})
    deleted = UserRepository.delete(str(user["_id"]))
    assert deleted is True
    assert UserRepository.get_by_id(str(user["_id"])) is None


def test_list_all():
    UserRepository.create({"username": "u1", "email": "u1@example.com"})
    UserRepository.create({"username": "u2", "email": "u2@example.com"})
    users = UserRepository.list_all()
    assert len(users) >= 2
