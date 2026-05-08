import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from bot import db

# Database Collections
users_db = db["users"]
groups_db = db["groups"]

#  Variable ထဲက OWNER_ID ကို ယူမယ်
try:
    OWNER_ID = int(os.environ.get("OWNER_ID", 0))
except:
    OWNER_ID = 0

# --- ၁။ ID များကို Database ထဲသိမ်းခြင်း ---
@Client.on_message(filters.command("start") & filters.private, group=10)
async def track_users(_, message: Message):
    await users_db.update_one(
        {"user_id": message.from_user.id}, 
        {"$set": {"user_id": message.from_user.id}}, 
        upsert=True
    )

@Client.on_message(filters.new_chat_members, group=11)
async def track_groups(_, message: Message):
    if message.new_chat_members:
        for member in message.new_chat_members:
            if member.is_self:
                await groups_db.update_one(
                    {"chat_id": message.chat.id}, 
                    {"$set": {"chat_id": message.chat.id}}, 
                    upsert=True
                )

# --- ၂။ Broadcast Command (Owner သီးသန့်) ---
@Client.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_msg(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("❌ Broadcast လုပ်မယ့်စာကို Reply ထောက်ပြီး `/broadcast` လို့ ရိုက်ပါ။")

    msg = message.reply_to_message
    status_msg = await message.reply_text("🚀 Broadcast စတင်နေပါပြီ... အလုပ်မလုပ်တော့တဲ့ ID တွေကိုပါ သန့်ရှင်းရေးလုပ်ပေးပါမယ်။")

    # --- User များဆီ ပို့ခြင်း ---
    u_count = 0
    u_failed = 0
    async for user in users_db.find():
        try:
            await msg.copy(chat_id=user["user_id"])
            u_count += 1
            await asyncio.sleep(0.3) 
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await msg.copy(chat_id=user["user_id"])
            u_count += 1
        except Exception:
            # Block ထားတဲ့သူကို Database ထဲက ဖျက်မယ်
            await users_db.delete_one({"user_id": user["user_id"]})
            u_failed += 1

    # --- Group များဆီ ပို့ခြင်း ---
    g_count = 0
    g_failed = 0
    async for group in groups_db.find():
        try:
            await msg.copy(chat_id=group["chat_id"])
            g_count += 1
            await asyncio.sleep(0.3)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await msg.copy(chat_id=group["chat_id"])
            g_count += 1
        except Exception:
            # Bot မရှိတော့တဲ့ Group ကို Database ထဲက ဖျက်မယ်
            await groups_db.delete_one({"chat_id": group["chat_id"]})
            g_failed += 1

    # --- ရလဒ်ပြသခြင်း ---
    report = (
        "✅ **Broadcast လုပ်ဆောင်ချက် ပြီးဆုံးပါပြီ!**\n\n"
        f"👤 **Users:**\n"
        f"   - အောင်မြင်: `{u_count}`\n"
        f"   - ဖယ်ရှားခဲ့သည် (Blocked): `{u_failed}`\n\n"
        f"👥 **Groups:**\n"
        f"   - အောင်မြင်: `{g_count}`\n"
        f"   - ဖယ်ရှားခဲ့သည် (Left/Kicked): `{g_failed}`"
    )
    await status_msg.edit_text(report)
