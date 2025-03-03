from pyrogram import Client
from commands import register_commands
import os
from dotenv import load_dotenv
from database import add_admin

# Load environment variables
load_dotenv()

# Debug: Print variables (remove this after testing)
print("API_ID:", os.getenv("API_ID"), "Type:", type(os.getenv("API_ID")))
print("ADMIN_ID:", os.getenv("ADMIN_ID"), "Type:", type(os.getenv("ADMIN_ID")))

# Ensure variables are not None
if not all([os.getenv("API_ID"), os.getenv("API_HASH"), os.getenv("BOT_TOKEN"), os.getenv("MONGO_URI"), os.getenv("ADMIN_ID")]):
    raise ValueError("One or more environment variables are missing. Check your .env file.")

app = Client(
    "bot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)

# Ensure the first admin is in the database
MAIN_ADMIN_ID = int(os.getenv("ADMIN_ID"))
add_admin(MAIN_ADMIN_ID)

register_commands(app)

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
