import os
import asyncio
from pyrogram import Client
from motor.motor_asyncio import AsyncIOMotorClient

# --- Environment Variables ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
MONGO_URL = os.environ.get("MONGO_URL", "")

# --- Database Setup ---
db_client = AsyncIOMotorClient(MONGO_URL)
db = db_client["Khh_db"]

# --- Bot Client Setup ---
# plugins=dict(root="plugins") လို့ ရေးထားရင် plugins folder ထဲက .py တွေကို အလိုအလျောက် ဖတ်ပေးပါလိမ့်မယ်
app = Client(
    "KHHPANDA_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins") 
)

if __name__ == "__main__":
    print("✅ MongoDB connection initiated.")
    print("✨ KHHPANDA Bot with Plugins is starting...")
    
    try:
        app.run()
    except Exception as e:
        print(f"❌ Critical Error: {e}")
