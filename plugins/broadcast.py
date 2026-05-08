import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from bot import db

# Database Collections
users_db = db["users"]
groups_db = db["groups"]

# Variable ထဲက OWNER_ID ကို ယူမယ်
try:
    OWNER_ID = int(os.environ.get("OWNER_ID", 0))
except:
    OWNER_ID = 0

# --- ၁။ ID များကို Database ထဲသိမ်းခြင်း ---
# Start လုပ်တဲ့ User ကို သိမ်းမယ်
@Client.on_message(filters.command("start") & filters.private, group=10)
async def track_users(_, message: Message):
    await users_db.update_one({"user_id": message.from_user.id}, {"$set": {"user_id": message.from_user.id}}, upsert=True)

# Group ထဲရောက်ရင် Group ID ကို သိမ်းမယ်
@Client.on_message(filters.new_chat_members, group=11)
async def track_groups(_, message: Message):
    if message.new_chat_members:
        for member in message.new_chat_members:
            if member.is_self:
                await groups_db.update_one({"chat_id": message.chat.id}, {"$set": {"chat_id": message.chat.id}}, upsert=True)

# --- ၂။ Broadcast Command (Owner သီးသန့်) ---
@Client.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_msg(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("❌ Broadcast လုပ်မယ့်စာကို Reply ထောက်ပြီး `/broadcast` လို့ ရိုက်ပါ။")

    msg = message.reply_to_message
    status_msg = await message.reply_text("🚀 Broadcast စတင်နေပါပြီ...")

    # User များဆီ ပို့ခြင်း
    users = users_db.find()
    u_count = 0
    async for user in users:
        try:
            await msg.copy(chat_id=user["user_id"])
            u_count += 1
            await asyncio.sleep(0.3) # Spam မဖြစ်အောင်
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except:
            pass

    # Group များဆီ ပို့ခြင်း
    groups = groups_db.find()
    g_count = 0
    async for group in groups:
        try:
            await msg.copy(chat_id=group["chat_id"])
            g_count += 1
            await asyncio.sleep(0.3)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except:
            pass

    await status_msg.edit_text(
        f"✅ **Broadcast ပြီးဆုံးပါပြီ!**\n\n"
        f"👤 Users: `{u_count}`\n"
        f"👥 Groups: `{g_count}`"
    )
