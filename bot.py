import os
from dotenv import load_dotenv
from pyrogram import Client

# Load environment variables
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Ensure API_ID is an integer
if not API_ID or not API_HASH or not BOT_TOKEN:
    raise ValueError("❌ Missing environment variables! Check .env or Docker settings.")

app = Client(
    "bot",
    api_id=int(API_ID),
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

if __name__ == "__main__":
    print("✅ Bot is running...")
    app.run()
