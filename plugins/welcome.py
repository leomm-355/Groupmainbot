import asyncio
from datetime import datetime
import pytz
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus
import os
from bot import db

# Railway Variable ထဲက OWNER_ID ကို ယူမယ်
OWNER_ID = int(os.environ.get("OWNER_ID", 0))

# Database collection
welcome_settings = db["welcome_settings"]

def get_now():
    tz = pytz.timezone('Asia/Yangon')
    return datetime.now(tz).strftime("%d/%m/%Y | %I:%M %p")

# --- ၁။ ပိတ်/ဖွင့် စနစ် (Admin & Owner သာ) ---
@Client.on_message(filters.command("welcome") & filters.group)
async def toggle_welcome(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Admin ဟုတ်မဟုတ် စစ်ဆေးခြင်း
    check_status = await client.get_chat_member(chat_id, user_id)
    is_admin = check_status.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    is_owner = (user_id == OWNER_ID)

    # Admin လည်းမဟုတ်၊ Bot Owner လည်းမဟုတ်ရင် ပယ်ချမယ်
    if not (is_admin or is_owner):
        return await message.reply("❌ ဒီ Command ကို Group Admin နဲ့ Bot Owner သာ အသုံးပြုနိုင်ပါတယ်။")

    if len(message.command) < 2:
        return await message.reply("💡 အသုံးပြုပုံ: `/welcome on` သို့မဟုတ် `/welcome off`")

    choice = message.command[1].lower()
    if choice == "on":
        await welcome_settings.update_one({"chat_id": chat_id}, {"$set": {"status": True}}, upsert=True)
        await message.reply("✅ **Welcome Message ကို ဖွင့်လိုက်ပါပြီ။**")
    elif choice == "off":
        await welcome_settings.update_one({"chat_id": chat_id}, {"$set": {"status": False}}, upsert=True)
        await message.reply("❌ **Welcome Message ကို ပိတ်လိုက်ပါပြီ။**")

# --- ၂။ Member အသစ်ဝင်လာရင် အလိုအလျောက် ကြိုဆိုခြင်း ---
@Client.on_message(filters.new_chat_members)
async def auto_welcome(client: Client, message: Message):
    # အရင်ဆုံး ဒီ Group မှာ Welcome ဖွင့်ထားလား Database မှာ စစ်မယ်
    chat_id = message.chat.id
    setting = await welcome_settings.find_one({"chat_id": chat_id})
    
    # Setting မရှိသေးရင် သို့မဟုတ် status က False ဖြစ်နေရင် ဘာမှမလုပ်ဘူး
    if setting and setting.get("status") is False:
        return

    for user in message.new_chat_members:
        if user.is_self: continue # Bot ကိုယ်တိုင်ဝင်တာဆိုရင် မပို့ဘူး

        welcome_text = (
            f"🎊 **မင်္ဂလာပါ၊ Group မှ ကြိုဆိုပါတယ်!**\n\n"
            f"👤 **အမည်:** {user.mention}\n"
            f"🆔 **ID:** `{user.id}`\n"
            f"⏰ **အချိန်:** {get_now()}\n\n"
            f"✨ **{message.chat.title}** မှာ ပျော်ရွှင်ပါစေဗျာ။"
        )

        # Welcome Photo (User ရဲ့ profile ပုံ၊ မရှိရင် Default ပုံ)
        photo = user.photo.big_file_id if user.photo else "https://files.catbox.moe/jebxwm.jpg"

        try:
            await message.reply_photo(photo=photo, caption=welcome_text)
        except Exception:
            await message.reply_text(welcome_text)
