from pyrogram import Client, filters
from database import add_user, get_users, set_welcome_message, get_welcome_message, add_admin, remove_admin, is_admin, get_admins
import os

def register_commands(app):
    @app.on_message(filters.private & filters.command("start"))
    async def start(client, message):
        add_user(message.chat.id)
        welcome_text = get_welcome_message()
        await message.reply_text(welcome_text)

    @app.on_message(filters.private & filters.command("setwelcome"))
    async def set_welcome(client, message):
        if not is_admin(message.chat.id):
            return await message.reply_text("❌ You are not an admin.")
        
        if len(message.command) < 2:
            return await message.reply_text("Usage: /setwelcome <new message>")
        
        new_message = " ".join(message.command[1:])
        set_welcome_message(new_message)
        await message.reply_text("✅ Welcome message updated!")

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
            return
