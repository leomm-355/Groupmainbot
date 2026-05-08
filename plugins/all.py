import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus

# လက်ရှိ Tag ခေါ်နေတဲ့ Group တွေကို မှတ်ထားဖို့
tag_proccess = []

@Client.on_message(filters.command("all") & filters.group)
async def mention_all(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    status_msg = await message.reply_text("⏳ Admin ဟုတ်မဟုတ် စစ်ဆေးနေပါတယ်...")

    try:
        check_admin = await client.get_chat_member(chat_id, user_id)
        if check_admin.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await status_msg.edit_text("❌ ဒီ Command ကို Group Admin များသာ အသုံးပြုနိုင်ပါတယ်။")

        input_text = message.text.split(None, 1)
        custom_message = input_text[1] if len(input_text) > 1 else "မင်္ဂလာပါ အားလုံးပဲ လာကြပါဦး ✨"

        await status_msg.edit_text("🚀 Member များကို Tag ခေါ်ပေးနေပါပြီ...\n\n(ရပ်တန့်လိုပါက `/stop` ဟု ရိုက်ပါ)")

        # ဒီ Group ကို Tag ခေါ်နေတဲ့စာရင်းထဲ ထည့်မယ်
        tag_proccess.append(chat_id)

        members = []
        async for member in client.get_chat_members(chat_id):
            if not member.user.is_bot and not member.user.is_deleted:
                members.append(member.user.mention)

        count = 0
        total_members = len(members)
        
        for i in range(0, total_members, 5):
            # အကယ်၍ /stop ရိုက်လိုက်ရင် ဒီထဲကနေ ထွက်သွားမယ်
            if chat_id not in tag_proccess:
                break
                
            chunk = members[i:i+5]
            mention_string = ", ".join(chunk)
            
            try:
                await client.send_message(
                    chat_id,
                    f"📢 **{custom_message}**\n\n"
                    f"✨ {mention_string}\n\n"
                    f"💡 စုစုပေါင်း: `{total_members}` ယောက်"
                )
                count += len(chunk)
                await asyncio.sleep(2.5) 
            except Exception:
                break

        # ပြီးသွားရင် (သို့မဟုတ် ရပ်လိုက်ရင်) စာရင်းထဲက ပြန်ထုတ်မယ်
        if chat_id in tag_proccess:
            tag_proccess.remove(chat_id)
            await status_msg.edit_text(f"✅ **Member {count} ယောက်ကို Tag ခေါ်ပြီးပါပြီ!**")
        else:
            await status_msg.edit_text(f"🛑 **Tag ခေါ်ခြင်းကို ရပ်တန့်လိုက်ပါပြီ။**\n(ခေါ်ပြီးသမျှ: `{count}` ယောက်)")
        
        await asyncio.sleep(10)
        await status_msg.delete()

    except Exception as e:
        if chat_id in tag_proccess: tag_proccess.remove(chat_id)
        await status_msg.edit_text(f"❌ Error: {e}")

# --- ၂။ Stop Command ---
@Client.on_message(filters.command("stop") & filters.group)
async def stop_tagging(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Admin ဟုတ်မှ ရပ်ခိုင်းလို့ရမယ်
    check_admin = await client.get_chat_member(chat_id, user_id)
    if check_admin.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return await message.reply_text("❌ Admin များသာ Tag ခေါ်ခြင်းကို ရပ်တန့်နိုင်ပါတယ်။")

    if chat_id in tag_proccess:
        tag_proccess.remove(chat_id)
        await message.reply_text("🛑 **Tag ခေါ်နေခြင်းကို ရပ်တန့်ရန် အမိန့်ပေးလိုက်ပါပြီ။**")
    else:
        await message.reply_text("💡 လက်ရှိမှာ Tag ခေါ်နေတာမျိုး မရှိပါဘူးဗျာ။")
