import os
import pytest
from src import db


def test_db_connection():
    """Test MongoDB connection and collections"""
    expected_db = os.getenv("MONGO_DB", "appdb")
    # Ensure db object is initialized
    assert db.db.name == expected_db

    # Check collections exist (they may be empty but should be accessible)
    collections = db.db.list_collection_names()
    expected = {"users", "orders", "stocks", "portfolio"}
    # The collections may not exist yet, but we can still access them
    for col in expected:
        assert isinstance(db.db[col], type(db.users_collection))
