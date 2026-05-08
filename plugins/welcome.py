import asyncio
import os
from datetime import datetime
import pytz
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus
from bot import db

# Railway Variable ထဲက OWNER_ID
OWNER_ID = int(os.environ.get("OWNER_ID", 0))
welcome_settings = db["welcome_settings"]

def get_now():
    tz = pytz.timezone('Asia/Yangon')
    return datetime.now(tz).strftime("%d/%m/%Y | %I:%M %p")

# --- ၁။ ပိတ်/ဖွင့် စနစ် (Admin & Owner သာ) ---
@Client.on_message(filters.command("welcome") & filters.group)
async def toggle_welcome(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    try:
        member = await client.get_chat_member(chat_id, user_id)
        is_group_admin = member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except:
        is_group_admin = False
        
    is_bot_owner = (user_id == OWNER_ID)

    if not (is_group_admin or is_bot_owner):
        return await message.reply_text("❌ ဒီ Command ကို Admin များသာ သုံးနိုင်ပါတယ်။")

    if len(message.command) < 2:
        return await message.reply_text("💡 `/welcome on` သို့မဟုတ် `/welcome off` ဟု သုံးပါ။")

    choice = message.command[1].lower()
    if choice == "on":
        await welcome_settings.update_one({"chat_id": chat_id}, {"$set": {"status": True}}, upsert=True)
        await message.reply_text("✅ Welcome စနစ်ကို **ဖွင့်လိုက်ပါပြီ**။")
    elif choice == "off":
        await welcome_settings.update_one({"chat_id": chat_id}, {"$set": {"status": False}}, upsert=True)
        await message.reply_text("❌ Welcome စနစ်ကို **ပိတ်လိုက်ပါပြီ**။")

# --- ၂။ Member အသစ်ဝင်လာရင် ကြိုဆိုခြင်း ---
@Client.on_message(filters.new_chat_members)
async def auto_welcome(client: Client, message: Message):
    chat_id = message.chat.id
    setting = await welcome_settings.find_one({"chat_id": chat_id})
    
    if setting and setting.get("status") is False:
        return

    for user in message.new_chat_members:
        if user.is_self: continue 

        welcome_text = (
            f"🎊 **မင်္ဂလာပါ၊ Group မှ ကြိုဆိုပါတယ်!**\n\n"
            f"👤 **အမည်:** {user.mention}\n"
            f"🆔 **ID:** `{user.id}`\n"
            f"⏰ **အချိန်:** {get_now()}\n\n"
            f"✨ **{message.chat.title}** မှာ ပျော်ရွှင်ပါစေဗျာ။"
        )
        
        # Add Me To Your Group Button
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Add Me To Your Group ➕", url=f"https://t.me/{client.me.username}?startgroup=true")]
        ])

        photo = user.photo.big_file_id if user.photo else "https://files.catbox.moe/jebxwm.jpg"
        try:
            await message.reply_photo(photo=photo, caption=welcome_text, reply_markup=buttons)
        except:
            await message.reply_text(welcome_text, reply_markup=buttons)

# --- ၃။ Member ထွက်သွားရင် နှုတ်ဆက်ခြင်း ---
@Client.on_message(filters.left_chat_member)
async def auto_goodbye(client: Client, message: Message):
    chat_id = message.chat.id
    setting = await welcome_settings.find_one({"chat_id": chat_id})
    
    if setting and setting.get("status") is False:
        return

    user = message.left_chat_member
    if user.is_self: return

    goodbye_text = (
        f"👋 **နှုတ်ဆက်ခဲ့ပါတယ်ဗျာ!**\n\n"
        f"👤 **အမည်:** {user.first_name}\n"
        f"🆔 **ID:** `{user.id}`\n"
        f"⏰ **အချိန်:** {get_now()}\n\n"
        "နောက်နောင်မှ ပြန်ဆုံကြတာပေါ့။"
    )

    try:
        await message.reply_text(goodbye_text)
    except:
        pass
