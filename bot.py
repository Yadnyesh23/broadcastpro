from pyrogram import Client
from commands import register_commands
import os
from dotenv import load_dotenv
from database import add_admin

# Load environment variables
load_dotenv()

# Retrieve environment variables
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
admin_id = os.getenv("ADMIN_ID")

# Print for debugging
print(f"API_ID: {api_id}, Type: {type(api_id)}")
print(f"ADMIN_ID: {admin_id}, Type: {type(admin_id)}")

# Ensure environment variables are present
if not api_id or not api_hash or not bot_token or not admin_id:
    raise ValueError("One or more environment variables are missing. Check your .env file.")

# Convert API_ID and ADMIN_ID to integers safely
try:
    API_ID = int(api_id.strip())  # Convert string to int, remove spaces if any
    ADMIN_ID = int(admin_id.strip())  # Convert string to int, remove spaces if any
except ValueError:
    raise ValueError("API_ID and ADMIN_ID must be valid integers.")

# Initialize bot
app = Client(
    "bot",
    api_id=API_ID,
    api_hash=api_hash,
    bot_token=bot_token
)

# Add admin to database
add_admin(ADMIN_ID)

# Register commands
register_commands(app)

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
