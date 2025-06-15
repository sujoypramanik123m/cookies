from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from database import db
from ffmpeg import compress_video
from utils import human_readable_size, progress_bar, time_formatter
import os
import asyncio
import time

@Client.on_message(filters.private & filters.video)
async def handle_video(client, message: Message):
    user_id = message.from_user.id
    user_tasks = await db.queue.count_documents({"user_id": user_id})

    if user_tasks >= 1:
        await message.reply("‼️ A Task Is Already In Progress.\nPlease Wait For It To Finish Before Starting A New One.")
        return

    total_tasks = await db.queue.count_documents({})
    if total_tasks >= Config.MAX_QUEUE_SIZE:
        position = total_tasks - Config.MAX_QUEUE_SIZE + 1
        await message.reply(
            f"5/5 Process running, Your video will be compressed soon😎.\n"
            f"Please wait until others' tasks are completed ✨\n\n📌 Your Task Has Been Added ✅\n⏳ Position In Queue: {position}"
        )
        await db.add_to_queue(user_id, message.video.file_id, message.video.file_name)
        return

    await db.add_to_queue(user_id, message.video.file_id, message.video.file_name)
    await process_queue(client)

async def process_queue(client):
    task = await db.get_next_in_queue()
    if not task:
        return

    user_id = task["user_id"]
    file_id = task["file_id"]
    file_name = task["file_name"]

    message = await client.send_message(user_id, "🚀 Trying To Download... ⚡")
    start_time = time.time()

    input_path = await client.download_media(file_id, file_name=file_name)
    await message.edit("🚀 Downloading... ⚡")

    # Simulate download progress
    await simulate_progress(message, start_time, os.path.getsize(input_path))

    output_path = f"compressed_{file_name}"
    await message.edit("🚀 Trying To Compress... ⚡")
    compressed_path = await compress_video(
        input_path, output_path, codec="libx265" if os.path.getsize(input_path) > 1e9 else "libx264"
    )

    if compressed_path:
        await message.edit("🚀 Trying To Upload... 💠")
        await client.send_video(user_id, compressed_path)
        await message.edit(
            f"✅ Upload Complete!\n\n🔗 Original Size: {human_readable_size(os.path.getsize(input_path))}\n"
            f"🔗 Compressed Size: {human_readable_size(os.path.getsize(compressed_path))}"
        )
        os.remove(compressed_path)

    os.remove(input_path)
    await message.delete()

async def simulate_progress(message, start_time, total_size):
    for i in range(1, 101):
        await asyncio.sleep(0.1)
        elapsed_time = time.time() - start_time
        speed = (total_size / 1024) / elapsed_time if elapsed_time > 0 else 0
        eta = (total_size / 1024) / speed if speed > 0 else 0
        progress = progress_bar(i, 100)
        await message.edit(
            f"{progress}\n\n🔗 Size : {human_readable_size(total_size)}\n⏳️ Done : {i}%\n"
            f"🚀 Speed : {round(speed, 2)} KB/s\n⏰️ ETA : {time_formatter(eta * 1000)}"
        )
