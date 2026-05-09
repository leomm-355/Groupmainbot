import os
from pyrogram import Client, filters
from pyrogram.types import Message

# Railway Variable ထဲက OWNER_ID ကို ယူမယ်
try:
    OWNER_ID = int(os.environ.get("OWNER_ID", 0))
except:
    OWNER_ID = 0

@Client.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    # --- ၁။ User များအတွက် (လူတိုင်းသုံးလို့ရတာ) ---
    help_text = "✨ **Bot Help Menu** ✨\n"
    help_text += "━━━━━━━━━━━━━━━━━━\n\n"
    help_text += "👤 **User Commands:**\n"
    help_text += "• `/id` - မိမိ ID ကိုကြည့်ရန်\n"
    help_text += "• `/couple` - groupတွင်သုံးရန်\n"
    help_text += "• `/happy` - groupတွင်ကြည့်ရန်\n"
    help_text += "• `/love` - အချစ်ရေးဟောရန်\n\n"

    # --- ၂။ Admin များအတွက် စစ်ဆေးခြင်း ---
    is_admin = False
    if message.chat.type in ["group", "supergroup"]:
        member = await client.get_chat_member(chat_id, user_id)
        if member.status in ["administrator", "creator"]:
            is_admin = True

    if is_admin or user_id == OWNER_ID:
        help_text += "👮 **Admin Commands:**\n"
        help_text += "• `/all` - အဖွဲ့ဝင်အားလုံးကို Tag ခေါ်ရန်\n"
        help_text += "• `/welcome on/off` - ကြိုဆိုစာစနစ်\n\n"

    # --- ၃။ Owner အတွက်သာ စစ်ဆေးခြင်း ---
    if user_id == OWNER_ID:
        help_text += "👑 **Owner Commands:**\n"
        help_text += "• `/broadcast` - သတင်းစကားပါးရန်\n"
        help_text += "• `/del` - အမေးအဖြေမှတ်ထားတာဖျက်ရန်\n\n"

    help_text += "━━━━━━━━━━━━━━━━━━\n"
    help_text += "💡 _Command များကို အသုံးပြုရန် စာရိုက်ကွက်တွင် ရိုက်ထည့်ပါ_"

    await message.reply_text(help_text)
