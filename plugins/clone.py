import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram.errors import UserNotParticipant

# --- CONFIGURATION ---
API_ID = int(os.getenv("API_ID", "12345"))
API_HASH = os.getenv("API_HASH", "your_hash")
OWNER_ID = int(os.getenv("OWNER_ID", "12345678"))
MONGO_URL = os.getenv("MONGO_URL")

# Channel Username များ ( @ မပါဘဲ ထည့်ပါ )
FORCE_CHANNELS = ["myanmar_music_Bot2027", "myanmarbot_music"] 

db_client = AsyncIOMotorClient(MONGO_URL)
db = db_client["CloneBotDB"]
tokens_col = db["tokens"]

running_clones = {}

async def start_clone_bot(bot_token):
    """Clone Bot ကို နှိုးပေးသည့် Function"""
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
    
    # --- Force Join စစ်ဆေးခြင်း ---
    not_joined = []
    for channel in FORCE_CHANNELS:
        try:
            await client.get_chat_member(channel, user_id)
        except UserNotParticipant:
            not_joined.append(channel)
        except:
            pass

    if not_joined:
        buttons = [[InlineKeyboardButton(f"Join {ch}", url=f"https://t.me/{ch}")] for ch in not_joined]
        return await message.reply_text(
            "⚠️ Clone ပွားနိုင်ရန် အောက်ပါ Channel (၂) ခုလုံးကို အရင် Join ပေးပါ။",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    if len(message.command) < 2:
        return await message.reply_text("အသုံးပြုပုံ: `/clone [BOT_TOKEN]`")

    bot_token = message.text.split(None, 1)[1].strip()
    msg = await message.reply_text("⌛ Clone စတင်နေပါသည်...")

    # DB မှာ သိမ်းမယ်
    await tokens_col.update_one({"token": bot_token}, {"$set": {"token": bot_token}}, upsert=True)

    success, result = await start_clone_bot(bot_token)
    if success:
        bot_info = await result.get_me()
        await msg.edit(f"🎉 **Clone အောင်မြင်ပါပြီ!**\n\n🤖 Bot: {bot_info.first_name}\n🆔 @{bot_info.username}")
    else:
        await msg.edit(f"❌ Error: {result}")

@Client.on_message(filters.command("restore") & filters.user(OWNER_ID))
async def restore_clones(client: Client, message: Message):
    """Bot Restart ဖြစ်သွားရင် Clone တွေ အကုန်ပြန်နှိုးဖို့"""
    msg = await message.reply_text("🔄 Database ထဲမှ Clone များကို ပြန်နှိုးနေပါသည်...")
    async for data in tokens_col.find():
        await start_clone_bot(data["token"])
    await msg.edit(f"✅ Clone Bot {len(running_clones)} ခုကို ပြန်နှိုးပြီးပါပြီ။")

@Client.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def bc_handler(client: Client, message: Message):
    """Owner တစ်ယောက်တည်းပဲ Clone အားလုံးကို Broadcast ခိုင်းမယ်"""
    if len(message.command) < 2:
        return await message.reply_text("`/broadcast [စာသား]`")
    
    text = message.text.split(None, 1)[1]
    await message.reply_text(f"🚀 Clone {len(running_clones)} ခုမှ Broadcast စတင်နေပြီ...")
    
    for bot_id in list(running_clones.keys()):
        bot = running_clones[bot_id]
        try:
            async for dialog in bot.get_dialogs():
                if dialog.chat.type in ["group", "supergroup"]:
                    await bot.send_message(dialog.chat.id, text)
                    await asyncio.sleep(0.3)
        except: continue
    await message.reply_text("✅ Broadcast ပို့ဆောင်ပြီးပါပြီ။")
