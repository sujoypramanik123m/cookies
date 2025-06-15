import os
from pyrogram import Client
from config import Config

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="video_compressor",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={
                "root": "plugins"
            },  # Ensure plugins directory is correctly set
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        print(f"{me.first_name} is Started.....✨️")

    async def stop(self):
        await super().stop()
        print("Bot is stopped.")

if __name__ == "__main__":
    Bot().run()