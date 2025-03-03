from pyrogram import Client, filters
from database import add_user, get_users, set_welcome_message, get_welcome_message, add_admin, remove_admin, is_admin, get_admins
import os
from pyrogram.types import Message

def register_commands(app):
    @app.on_message(filters.private & filters.command("start"))
    async def start(client, message):
        add_user(message.chat.id)
        welcome_text = get_welcome_message()
        await message.reply_text(welcome_text)

    # Create a directory for saving photos (if it doesn't already exist)
    PHOTO_STORAGE_DIR = "photos"
    if not os.path.exists(PHOTO_STORAGE_DIR):
        os.makedirs(PHOTO_STORAGE_DIR)

    @app.on_message(filters.private & filters.command("start"))
    async def start(client, message):
        add_user(message.chat.id)
        welcome_message = get_welcome_message()

        # Check if the welcome message is a photo path (not file_id)
        if welcome_message and welcome_message.startswith("photo_"):
            photo_file_path = welcome_message.split("_")[1]
            try:
                await message.reply_photo(photo_file_path)  # Send the photo by file path
            except ValueError:
                await message.reply_text("❌ Failed to send the photo. The file might have been removed.")
        else:
            await message.reply_text(welcome_message)  # Send as text

    @app.on_message(filters.private & filters.command("setwelcome"))
    async def set_welcome(client, message: Message):
        if not is_admin(message.chat.id):
            return await message.reply_text("❌ You are not an admin.")
        
        # If it's a text message
        if len(message.command) >= 2 and not any([message.photo, message.audio, message.video]):
            new_message = " ".join(message.command[1:])
            set_welcome_message(new_message)
            await message.reply_text("✅ Welcome message updated!")
        
        # If it's a photo
        elif message.photo:
            # Download the photo to the server
            photo = message.photo
            downloaded_photo_path = os.path.join(PHOTO_STORAGE_DIR, f"{photo.file_id}.jpg")
            await message.download(downloaded_photo_path)
            
            # Save the path of the downloaded photo
            set_welcome_message(f"photo_{downloaded_photo_path}")
            await message.reply_text("✅ Welcome photo updated!")

        # If it's an audio message
        elif message.audio:
            audio_file_id = message.audio.file_id
            set_welcome_message(f"audio_{audio_file_id}")  # Store the file ID with prefix
            await message.reply_text("✅ Welcome audio updated.")
        
        # If it's a video message
        elif message.video:
            video_file_id = message.video.file_id
            set_welcome_message(f"video_{video_file_id}")  # Store the file ID with prefix
            await message.reply_text("✅ Welcome video updated.")
    
    # Keep other commands as they are...
    @app.on_message(filters.private & filters.command("broadcast"))
    async def broadcast(client, message):
        if not is_admin(message.chat.id):
            return await message.reply_text("❌ You are not an admin.")
        
        if len(message.command) < 2:
            return await message.reply_text("Usage: /broadcast <message>")
        
        msg = " ".join(message.command[1:])
        users = get_users()
        
        sent, failed = 0, 0
        for user in users:
            try:
                await client.send_message(user["user_id"], msg)
                sent += 1
            except:
                failed += 1
        
        await message.reply_text(f"📢 Broadcast completed:\n✅ Sent: {sent}\n❌ Failed: {failed}")

    @app.on_message(filters.private & filters.command("addadmin"))
    async def add_admin_command(client, message):
        if not is_admin(message.chat.id):
            return await message.reply_text("❌ You are not an admin.")
        
        if len(message.command) < 2:
            return await message.reply_text("Usage: /addadmin <user_id>")
        
        try:
            new_admin_id = int(message.command[1])
            add_admin(new_admin_id)
            await message.reply_text(f"✅ User {new_admin_id} is now an admin!")
        except ValueError:
            await message.reply_text("❌ Invalid user ID format.")
    
    @app.on_message(filters.private & filters.command("removeadmin"))
    async def remove_admin_command(client, message):
        if not is_admin(message.chat.id):
            return await message.reply_text("❌ You are not an admin.")
        
        if len(message.command) < 2:
            return await message.reply_text("Usage: /removeadmin <user_id>")
        
        try:
            admin_id = int(message.command[1])
            if admin_id == message.chat.id:
                return await message.reply_text("❌ You cannot remove yourself.")
            
            remove_admin(admin_id)
            await message.reply_text(f"✅ User {admin_id} is no longer an admin!")
        except ValueError:
            await message.reply_text("❌ Invalid user ID format.")
    
    @app.on_message(filters.private & filters.command("listadmins"))
    async def list_admins(client, message):
        if not is_admin(message.chat.id):
            return await message.reply_text("❌ You are not an admin.")
        
        admins = get_admins()
        if not admins:
            return await message.reply_text("No admins found.")
        
        admin_list = "\n".join([str(admin["user_id"]) for admin in admins])
        await message.reply_text(f"List of Admins:\n{admin_list}")

    @app.on_message(filters.private & filters.command("commands"))
    async def show_commands(client, message):
        if not is_admin(message.chat.id):
            return await message.reply_text("❌ You are not an admin.")
        
        commands_list = """
        Available Commands:
        
        /start - Start the bot and receive the welcome message.
        /setwelcome - Set the welcome message (text, photo, audio, video).
        /broadcast - Broadcast a message to all users.
        /addadmin - Add a new admin.
        /removeadmin - Remove an existing admin.
        /listadmins - List all admins.
        /commands - Show available commands for admins.
        """
        
        await message.reply_text(commands_list)
