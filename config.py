import os
import time
import re

id_pattern = re.compile(r"^-?\d+$")

class Config(object):
    API_ID = os.environ.get("API_ID", "22182189")
    API_HASH = os.environ.get("API_HASH", "5e7c4088f8e23d0ab61e29ae11960bf5")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7863236360:AAEY4TX71CqK664bIx7b3S8xpswB-0q3y2s")
    DB_URL = os.environ.get("DB_URL", "mongodb+srv://sujoy123m:wTWKGUaxYE7dxb1l@cluster0.zorxb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    DB_NAME = os.environ.get("DB_NAME", "video_compressor")
    ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get("ADMIN", "8181241262").split()]
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002872961182"))
    BOT_UPTIME = time.time()
    MAX_QUEUE_SIZE = 5
