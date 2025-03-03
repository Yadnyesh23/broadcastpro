from pyrogram import Client
from commands import register_commands
import os
from dotenv import load_dotenv

load_dotenv()

app = Client(
    "bot",
    api_id=os.getenv("API_ID"),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)

register_commands(app)

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
