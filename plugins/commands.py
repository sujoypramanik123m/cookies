from pyrogram import Client, filters
from config import Config
from database import db
import os
import sys
import time
import asyncio

@Client.on_message(filters.command("status") & filters.user(Config.ADMIN))
async def get_stats(client, message):
    total_users = await db.total_users()
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - Config.BOT_UPTIME))
    await message.reply(f"Bot Stats:\n\nUptime: {uptime}\nTotal Users: {total_users}")

@Client.on_message(filters.command("restart") & filters.user(Config.ADMIN))
async def restart_bot(client, message):
    await message.reply("🔄 Restarting the bot...")
    os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMIN) & filters.reply)
async def broadcast_handler(client, message):
    all_users = await db.get_all_users()
    broadcast_msg = message.reply_to_message
    for user in all_users:
        try:
            await client.send_message(user["_id"], broadcast_msg.text)
        except:
            pass
    await message.reply("✅ Broadcast completed.")

@Client.on_message(filters.command("ban") & filters.user(Config.ADMIN))
async def ban_user(client, message):
    if len(message.command) < 2:
        await message.reply("Please specify the user ID to ban.")
        return
    user_id = int(message.command[1])
    await db.ban_user(user_id)
    await message.reply(f"✅ User {user_id} has been banned.")

@Client.on_message(filters.command("unban") & filters.user(Config.ADMIN))
async def unban_user(client, message):
    if len(message.command) < 2:
        await message.reply("Please specify the user ID to unban.")
        return
    user_id = int(message.command[1])
    await db.unban_user(user_id)
    await message.reply(f"✅ User {user_id} has been unbanned.")
