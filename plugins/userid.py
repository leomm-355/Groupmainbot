from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command(["id", "info"]) & (filters.group | filters.private))
async def get_user_info(client: Client, message: Message):
    # Reply ရှိရင် reply လုပ်ခံရသူ၊ မရှိရင် Command ရိုက်သူရဲ့ ID ကို ယူမယ်
    if message.reply_to_message:
        target_id = message.reply_to_message.from_user.id
    else:
        target_id = message.from_user.id
    
    try:
        # Chat info ကနေ Bio/Description ကို ဆွဲယူမယ်
        user_info = await client.get_chat(target_id)
        
        user_id = user_info.id
        first_name = user_info.first_name
        last_name = user_info.last_name if user_info.last_name else ""
        username = f"@{user_info.username}" if user_info.username else "မရှိပါ"
        
        # Bio ကို နည်းလမ်းမျိုးစုံနဲ့ စစ်ဆေးမယ်
        bio = getattr(user_info, "bio", None) or getattr(user_info, "description", None) or "မရှိပါ"
        
        # Premium Status အတွက် get_users ကို သုံးမယ်
        user_obj = await client.get_users(target_id)
        is_premium = "ရှိပါသည် ✅" if user_obj.is_premium else "မရှိပါ ❌"
        
        info_text = (
            "✨ **User Information** ✨\n"
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
        
    except Exception as e:
        # Error တက်ခဲ့ရင် (ဥပမာ User က Bot ကို Block ထားတာမျိုး)
        await message.reply_text(f"❌ အချက်အလက် ရှာမတွေ့ပါ သို့မဟုတ် Error ဖြစ်သွားပါသည်: {e}")
