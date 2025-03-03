from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))
db = client["telegram_bot"]
users_collection = db["users"]
settings_collection = db["settings"]
admins_collection = db["admins"]

def add_user(user_id):
    """Store user ID in the database."""
    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({"user_id": user_id})

def get_users():
    """Retrieve all registered users."""
    return users_collection.find({}, {"_id": 0, "user_id": 1})

def set_welcome_message(message):
    """Update the welcome message."""
    settings_collection.update_one({}, {"$set": {"welcome_message": message}}, upsert=True)

def get_welcome_message():
    """Fetch the stored welcome message or return default."""
    msg = settings_collection.find_one({}, {"_id": 0, "welcome_message": 1})
    return msg["welcome_message"] if msg else "Hello! Welcome to the bot!"

def add_admin(user_id):
    """Add a new admin."""
    if not admins_collection.find_one({"user_id": user_id}):
        admins_collection.insert_one({"user_id": user_id})

def remove_admin(user_id):
    """Remove an admin."""
    admins_collection.delete_one({"user_id": user_id})

def is_admin(user_id):
    """Check if a user is an admin."""
    return admins_collection.find_one({"user_id": user_id}) is not None

def get_admins():
    """Get all admin IDs."""
    return [admin["user_id"] for admin in admins_collection.find({}, {"_id": 0, "user_id": 1})]
