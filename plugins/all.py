import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus

# --- ၁။ Tag All စနစ် ---
@Client.on_message(filters.command("all") & filters.group)
async def mention_all(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Loading စာသားအရင်ပြမယ်
    status_msg = await message.reply_text("⏳ Admin ဟုတ်မဟုတ် စစ်ဆေးနေပါတယ်...")

    try:
        # Admin ဟုတ်မဟုတ် စစ်ဆေးခြင်း
        check_admin = await client.get_chat_member(chat_id, user_id)
        
        # Admin လည်းမဟုတ်၊ Owner လည်းမဟုတ်ရင် ပြန်ထွက်မယ်
        if check_admin.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await status_msg.edit_text("❌ ဒီ Command ကို Group Admin များသာ အသုံးပြုနိုင်ပါတယ်။")

        # ကိုယ်တိုင်ရေးချင်တဲ့စာ (ဥပမာ - /all အားလုံးတက်လာကြ)
        input_text = message.text.split(None, 1)
        custom_message = input_text[1] if len(input_text) > 1 else "မင်္ဂလာပါ အားလုံးပဲ လာကြပါဦး ✨"

        await status_msg.edit_text("🚀 Member များကို Tag ခေါ်ပေးနေပါပြီ...")

        # Member စာရင်းကို ဆွဲထုတ်မယ်
        members = []
        async for member in client.get_chat_members(chat_id):
            if not member.user.is_bot and not member.user.is_deleted:
                members.append(member.user.mention)

        # ၅ ယောက်တစ်တွဲစီ Tag ခေါ်မယ် (Spam/Flood မဖြစ်အောင်)
        count = 0
        total_members = len(members)
        
        for i in range(0, total_members, 5):
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
                await asyncio.sleep(2.5) # Telegram က Ban မလုပ်အောင် အချိန်ခဏခြားမယ်
            except Exception:
                break

        await status_msg.edit_text(f"✅ **Member {count} ယောက်ကို Tag ခေါ်ပြီးပါပြီ!**")
        
        # ၁၀ စက္ကန့်ကြာရင် Report စာသားကို ဖျက်မယ်
        await asyncio.sleep(10)
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f"❌ Error: {e}")
