from pyrogram import Client
from commands import register_commands
import os
from dotenv import load_dotenv

load_dotenv()

# Convert API_ID to int
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

register_commands(app)

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
