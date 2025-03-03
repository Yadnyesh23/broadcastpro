from pyrogram import Client
from commands import register_commands
import os
from dotenv import load_dotenv
from database import add_admin

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
admin_id = os.getenv("ADMIN_ID")

# Validate environment variables
if not api_id or not api_hash or not bot_token or not admin_id:
    raise ValueError("One or more environment variables are missing. Check your .env file.")

# Convert ADMIN_ID to an integer safely
try:
    MAIN_ADMIN_ID = int(admin_id)
except ValueError:
    raise ValueError("ADMIN_ID must be a valid integer.")

# Initialize the bot
app = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

# Ensure the first admin (you) is in the database
add_admin(MAIN_ADMIN_ID)

# Register bot commands
register_commands(app)

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
