from pyrogram import Client, filters
from dotenv import load_dotenv
import os

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

app = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
def start(client, message):
    message.reply("Hello! I'm your bot!")

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
