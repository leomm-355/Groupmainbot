from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command(["id", "info"]) & filters.group)
async def get_user_info(client: Client, message: Message):
    # Reply ပြန်ထားတဲ့ message ရှိရင် အဲ့ဒီလူရဲ့ info ကိုယူမယ်
    # မရှိရင် command ရိုက်တဲ့သူရဲ့ info ကိုယူမယ်
    target_user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    
    # User ရဲ့ အသေးစိတ် အချက်အလက်ကို ထပ်မံရယူခြင်း (Bio သိရအောင်)
    full_user = await client.get_users(target_user.id)
    
    # အချက်အလက်များ ထုတ်ယူခြင်း
    user_id = full_user.id
    first_name = full_user.first_name
    last_name = full_user.last_name if full_user.last_name else ""
    username = f"@{full_user.username}" if full_user.username else "မရှိပါ"
    bio = full_user.bio if full_user.bio else "Bio ရေးမထားပါ"
    is_premium = "ရှိပါသည် ✅" if full_user.is_premium else "မရှိပါ ❌"
    
    # စာသားအလှဆင်ခြင်း
    info_text = (
        "✨ **Information** ✨\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"👤 **အမည်:** {first_name} {last_name}\n"
        f"🆔 **User ID:** `{user_id}`\n"
        f"🔗 **Username:** {username}\n"
        f"📝 **Bio:** \n_{bio}_\n\n"
        f"🌟 **Premium:** {is_premium}\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"✨ **Requested by:** {message.from_user.mention}"
    )
    
    await message.reply_text(info_text)

# Private Chat မှာလည်း သုံးလို့ရအောင် ထပ်ရေးပေးထားခြင်း
@Client.on_message(filters.command(["id", "info"]) & filters.private)
async def get_info_pv(client: Client, message: Message):
    full_user = await client.get_users(message.from_user.id)
    
    info_text = (
        "✨ **Information** ✨\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"👤 **အမည်:** {full_user.first_name}\n"
        f"🆔 **User ID:** `{full_user.id}`\n"
        f"🔗 **Username:** @{full_user.username if full_user.username else 'မရှိပါ'}\n"
        f"📝 **Bio:** \n_{full_user.bio if full_user.bio else 'မရှိပါ'}_\n\n"
        f"🌟 **Premium:** {'ရှိပါသည် ✅' if full_user.is_premium else 'မရှိပါ ❌'}\n"
        "━━━━━━━━━━━━━━━━━━"
    )
    
    await message.reply_text(info_text)
