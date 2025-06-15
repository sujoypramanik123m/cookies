import motor.motor_asyncio
from config import Config

class Database:
    def __init__(self, uri, database_name):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client[database_name]
        self.queue = self.db.queue
        self.users = self.db.users

    async def add_to_queue(self, user_id, file_id, file_name):
        await self.queue.insert_one({"user_id": user_id, "file_id": file_id, "file_name": file_name})

    async def get_next_in_queue(self):
        return await self.queue.find_one_and_delete({})

    async def add_user(self, user_id):
        if not await self.users.find_one({"_id": user_id}):
            await self.users.insert_one({"_id": user_id})

    async def total_users(self):
        return await self.users.count_documents({})

db = Database(Config.DB_URL, Config.DB_NAME)
