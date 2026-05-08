import os
import asyncio
import time
from pyrogram import Client
from motor.motor_asyncio import AsyncIOMotorClient


API_ID = int(os.environ.get("API_ID", 12345))
API_HASH = os.environ.get("API_HASH", "your_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_token")
MONGO_URL = os.environ.get("MONGO_URL")


db_client = AsyncIOMotorClient(MONGO_URL)
db = db_client["Khh_db"]


app = Client(
    "KHHPANDA_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins") 
)

if __name__ == "__main__":
    while True:
        try:
            print("Bot with Plugins is starting...")
            app.run()
        except Exception as e:
            print(f"Crashed: {e}")
            time.sleep(5)
            continue

#KhitHlainHtet
