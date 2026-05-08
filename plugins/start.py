import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# --- Configuration ---
DEFAULT_PHOTO = "https://files.catbox.moe/jebxwm.jpg" 
WELCOME_STICKER = "CAACAgUAAxkBAAIe72mqfmL7cPOdiA5TOr6Gsih09cVTAALgGQACfA2YVRl1rlBfNwT5HgQ"

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    #
    text = "မဂ်လာပါ အချစ်လေး ပူတူးတူးလေး သေးသေးလေး"
    typing_msg = await message.reply_text("...")
    
    display_text = ""
    for char in text:
        display_text += char
        try:
            await typing_msg.edit_text(display_text)
            await asyncio.sleep(0.1) # စာလုံးပေါ်နှုန်း (0.1 စက္ကန့်)
        except:
            pass
    
    await asyncio.sleep(1) # ခဏစောင့်မယ်
    await typing_msg.delete() # စာသားကို ပြန်ဖျက်မယ်

    # ၂။ Sticker ပို့မယ်
    try:
        sent_stk = await message.reply_sticker(WELCOME_STICKER)
        await asyncio.sleep(5) # ၅ စက္ကန့် စောင့်မယ်
        await sent_stk.delete() # Sticker ကို ပြန်ဖျက်မယ်
    except Exception as e:
        print(f"Sticker Error: {e}")

    # ၃။ နောက်ဆုံး ပုံ၊ စာသား နဲ့ Button ၅ ခု ပို့မယ်
    user = message.from_user
    user_name = user.first_name if user.first_name else "User"
    
    welcome_final = (
        f"Welcome {user.mention} ✨\n\n"
        "**အချစ်များ** မှ ကြိုဆိုပါတယ်ဗျာ။\n"
        "Auto Reply နဲ့ Group Management Bot တစ်ခုဖြစ်ပါတယ်။\n"
        "အချစ်ရေးများလည်းမေးလို့ရပါတယ် /love ဖြင့်။\n"
        "သိလိုရာများကို /help  တွေကိုနှိပ်ပြီး လေ့လာနိုင်ပါတယ်ဗျာ။"
    )

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Channel 📢", url="https://t.me/myanmarbot_music"),
            InlineKeyboardButton("Developer 👨‍💻", url="http://t.me/HANTHAR999")
        ],
        [
            InlineKeyboardButton("Group 👥", url="https://t.me/myanmar_music_Bot2027"),
            InlineKeyboardButton("🌐 Update", url="https://t.me/myanmarbot_music/29")
        ],
        [
            InlineKeyboardButton("Add Me To Your Group ➕", url=f"https://t.me/{client.me.username}?startgroup=true")
        ]
    ])

    photo_to_send = DEFAULT_PHOTO
    if user.photo:
        photo_to_send = user.photo.big_file_id

    try:
        await message.reply_photo(
            photo=photo_to_send,
            caption=welcome_final,
            reply_markup=buttons
        )
    except Exception as e:
        await message.reply_text(welcome_final, reply_markup=buttons)
