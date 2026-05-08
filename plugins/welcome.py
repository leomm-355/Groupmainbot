import asyncio
from datetime import datetime
import pytz
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import db # bot.py ထဲက db ကို လှမ်းသုံးမယ်

# --- Configuration ---
DEFAULT_PHOTO = "https://files.catbox.moe/jebxwm.jpg" 
welcome_settings = db["welcome_settings"]

# အချိန်ကို မြန်မာစံတော်ချိန်နဲ့ ယူဖို့
def get_now():
    tz = pytz.timezone('Asia/Yangon')
    return datetime.now(tz).strftime("%d/%m/%Y | %I:%M %p")

# --- 1. Welcome On/Off Command ---
@Client.on_message(filters.command("welcome") & filters.group)
async def toggle_welcome(client: Client, message: Message):
    # Owner ဒါမှမဟုတ် Admin ဟုတ်မဟုတ် စစ်မယ်
    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in ["administrator", "creator"]:
        return await message.reply("ဒီ Command ကို Admin တွေပဲ သုံးလို့ရပါတယ်။")

    if len(message.command) < 2:
        return await message.reply("အသုံးပြုပုံ: `/welcome on` သို့မဟုတ် `/welcome off`")

    choice = message.command[1].lower()
    if choice == "on":
        await welcome_settings.update_one({"chat_id": message.chat.id}, {"$set": {"status": True}}, upsert=True)
        await message.reply("✅ ဒီ Group အတွက် Welcome Message ကို **ဖွင့်လိုက်ပါပြီ**။")
    elif choice == "off":
        await welcome_settings.update_one({"chat_id": message.chat.id}, {"$set": {"status": False}}, upsert=True)
        await message.reply("❌ ဒီ Group အတွက် Welcome Message ကို **ပိတ်လိုက်ပါပြီ**။")

# --- 2. New Member Welcome ---
@Client.on_message(filters.new_chat_members)
async def welcome_member(client: Client, message: Message):
    # Setting စစ်မယ်
    setting = await welcome_settings.find_one({"chat_id": message.chat.id})
    if setting and not setting.get("status", True):
        return

    for user in message.new_chat_members:
        # Bot ကိုယ်တိုင်ဆိုရင် မပို့ဘူး
        if user.is_self: continue

        welcome_text = (
            f"🎉 **ပျော်ရွှင်ပါစေ၊ ကြိုဆိုပါတယ်ဗျာ!**\n\n"
            f"👤 **အမည်:** {user.mention}\n"
            f"🆔 **ID:** `{user.id}`\n"
            f"👥 **Group:** {message.chat.title}\n"
            f"⏰ **အချိန်:** {get_now()}\n\n"
            "ကျွန်တော့်ကိုလည်း သင်ပိုင်ဆိုင်တဲ့ Group ထဲ ထည့်လို့ရပါတယ်နော်!"
        )

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Add Me To Your Group ➕", url=f"https://t.me/{client.me.username}?startgroup=true")]
        ])

        photo = user.photo.big_file_id if user.photo else DEFAULT_PHOTO
        
        try:
            await message.reply_photo(photo=photo, caption=welcome_text, reply_markup=buttons)
        except:
            await message.reply_text(welcome_text, reply_markup=buttons)

# --- 3. Left Member Farewell ---
@Client.on_message(filters.left_chat_member)
async def goodbye_member(client: Client, message: Message):
    # Setting စစ်မယ်
    setting = await welcome_settings.find_one({"chat_id": message.chat.id})
    if setting and not setting.get("status", True):
        return

    user = message.left_chat_member
    if user.is_self: return

    goodbye_text = (
        f"👋 **Group ထဲက ထွက်ခွာသွားပါပြီ...**\n\n"
        f"👤 **အမည်:** {user.first_name if user.first_name else 'User'}\n"
        f"🆔 **ID:** `{user.id}`\n"
        f"👥 **Group:** {message.chat.title}\n"
        f"⏰ **အချိန်:** {get_now()}\n\n"
        "နောက်နောင်မှ ပြန်ဆုံကြတာပေါ့ဗျာ။"
    )

    photo = user.photo.big_file_id if user.photo else DEFAULT_PHOTO

    try:
        await message.reply_photo(photo=photo, caption=goodbye_text)
    except:
        await message.reply_text(goodbye_text)
