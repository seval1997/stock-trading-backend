import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "appdb")

# Initialize MongoDB client
client = MongoClient(MONGO_URI)

# Reference to the database
db = client[MONGO_DB]

# Example: collections
users_collection = db["users"]
orders_collection = db["orders"]
stocks_collection = db["stocks"]
portfolio_collection = db["portfolio"]