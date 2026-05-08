from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command(["id", "info"]))
async def get_user_info(client: Client, message: Message):
    # Reply ရှိရင် reply လူ၊ မရှိရင် command ရိုက်တဲ့လူ
    target_id = message.reply_to_message.from_user.id if message.reply_to_message else message.from_user.id
    
    try:
        # Chat info ကနေ ယူမှ Bio (description/about) ကို ရနိုင်မှာပါ
        user_info = await client.get_chat(target_id)
        
        user_id = user_info.id
        first_name = user_info.first_name
        last_name = user_info.last_name if user_info.last_name else ""
        username = f"@{user_info.username}" if user_info.username else "မရှိပါ"
        
        # Bio ကို ယူတဲ့နေရာမှာ bio (သို့) description (သို့) about တစ်ခုခု ဖြစ်နိုင်လို့ စစ်ပေးထားပါတယ်
        bio = user_info.bio or user_info.description or "မရှိပါ"
        
        # Premium status ကတော့ get_users ကနေပဲ ရမှာမို့ တစ်ခါပြန်စစ်ပါမယ်
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
        await message.reply_text(f"❌ Error ဖြစ်သွားပါသည်: {e}")
