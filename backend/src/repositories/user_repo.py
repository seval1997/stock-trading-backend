from typing import Optional, Dict, Any
from bson import ObjectId
from src.db import db


class UserRepository:
    collection = db["users"]

    @staticmethod
    def create(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a new user document."""
        result = UserRepository.collection.insert_one(user_data)
        user_data["_id"] = result.inserted_id
        return user_data

    @staticmethod
    def get_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        """Fetch user by MongoDB ObjectId."""
        return UserRepository.collection.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def get_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Fetch user by email."""
        return UserRepository.collection.find_one({"email": email})

    @staticmethod
    def get_by_username(username: str) -> Optional[Dict[str, Any]]:
        """Fetch user by username."""
        return UserRepository.collection.find_one({"username": username})

    @staticmethod
    def update(user_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update user fields."""
        UserRepository.collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": update_data}
        )
        return UserRepository.get_by_id(user_id)

    @staticmethod
    def delete(user_id: str) -> bool:
        """Delete user by ID."""
        result = UserRepository.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0

    @staticmethod
    def list_all(limit: int = 50) -> list[Dict[str, Any]]:
        """List all users (paginated)."""
        return list(UserRepository.collection.find().limit(limit))
