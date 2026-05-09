from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command(["id", "info"]) & (filters.group | filters.private))
async def get_user_info(client: Client, message: Message):
    # --- ၁။ ID သတ်မှတ်ခြင်း ---
    # Reply ရှိရင် reply လုပ်ခံရသူ၊ မရှိရင် Command ရိုက်သူ
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
    else:
        target_user = message.from_user

    # User ID မရှိတဲ့ Message မျိုးဆိုရင် (ဥပမာ Channel Post)
    if not target_user:
        return await message.reply_text("❌ User ID ကို ရှာမတွေ့ပါ။")

    try:
        # --- ၂။ အချက်အလက်များ ရယူခြင်း ---
        # User အသေးစိတ်ကို get_users နဲ့ ယူတာက ပိုစိတ်ချရတယ်
        user_obj = await client.get_users(target_user.id)
        
        user_id = user_obj.id
        first_name = user_obj.first_name
        last_name = user_obj.last_name if user_obj.last_name else ""
        username = f"@{user_obj.username}" if user_obj.username else "မရှိပါ"
        is_premium = "ရှိပါသည် ✅" if user_obj.is_premium else "မရှိပါ ❌"
        
        # Group ID ကို ယူမယ် (Private Chat ဆိုရင် User ID ပဲ ထပ်ပြမယ်)
        chat_id = message.chat.id
        chat_title = message.chat.title if message.chat.title else "Private Chat"
        
        # Bio ကိုယူဖို့ get_chat သုံးမယ် (Error တက်နိုင်လို့ try-except ပတ်ထားမယ်)
        try:
            full_chat = await client.get_chat(user_id)
            bio = full_chat.bio if hasattr(full_chat, "bio") else "မရှိပါ"
        except:
            bio = "မရှိပါ (သို့) Bot ကို Block ထားပါသည်"

        # --- ၃။ စာသား ပြင်ဆင်ခြင်း ---
        info_text = (
            "✨ **User Information** ✨\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"👤 **အမည်:** {first_name} {last_name}\n"
            f"🆔 **User ID:** `{user_id}`\n"
            f"🔗 **Username:** {username}\n"
            f"📝 **Bio:** \n_{bio}_\n"
            f"🌟 **Premium:** {is_premium}\n\n"
            "👥 **Group Information**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"🏷️ **Group Name:** {chat_title}\n"
            f"🆔 **Group ID:** `{chat_id}`\n\n"
            f"✨ **Requested by:** {message.from_user.mention}"
        )
        
        await message.reply_text(info_text)
        
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
