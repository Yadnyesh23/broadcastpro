from pyrogram import Client
from commands import register_commands
from dotenv import load_dotenv
import os

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

app = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

register_commands(app)

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
