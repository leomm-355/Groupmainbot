import os
import asyncio
import time
from pyrogram import Client
from motor.motor_asyncio import AsyncIOMotorClient


API_ID = int(os.environ.get("API_ID", 12345))
API_HASH = os.environ.get("API_HASH", "your_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_token")
MONGO_URL = os.environ.get("MONGO_URL")

# --- Database Setup ---
db = None
if MONGO_URL:
    try:
        db_client = AsyncIOMotorClient(MONGO_URL)
        db = db_client["Khh_db"]
        print("✅ MongoDB connection initiated.")
    except Exception as e:
        print(f"❌ MongoDB initialization failed: {e}")
else:
    
    print("❌ Error: MONGO_URL is missing in Railway Variables!")

# --- Bot Client ---
app = Client(
    "KHHPANDA_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins") 
)

# --- Start System with Auto-Restart ---
if __name__ == "__main__":
    while True:
        try:
            print("✨ KHHPANDA Bot with Plugins is starting...")
            app.run()
        except Exception as e:
            
            print(f"⚠️ Bot Crashed: {e}")
            print("🔄 Restarting in 5 seconds...")
            time.sleep(5)
            continue

# KhitHlainHtet
