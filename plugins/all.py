import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("all") & filters.group)
async def mention_all(client: Client, message: Message):
    # ၁။ Admin/Owner ဟုတ်မဟုတ် အရင်စစ်မယ်
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    check_admin = await client.get_chat_member(chat_id, user_id)
    if check_admin.status not in ["administrator", "creator"]:
        return await message.reply_text("❌ ဒီ Command ကို Group Admin များသာ အသုံးပြုနိုင်ပါတယ်။")

    # ၂။ ကိုယ်ပြောချင်တဲ့ စာသားကို Command ဘေးမှာ ရေးထားလား စစ်မယ်
    # ဥပမာ - /all ဟိုင်း အားလုံးပဲ မင်္ဂလာပါ
    input_text = message.text.split(None, 1)
    custom_message = input_text[1] if len(input_text) > 1 else "လာကြပါဗျို့ ✨"

    # ၃။ Loading ပြမယ်
    status_msg = await message.reply_text("🚀 **Member တွေကို Tag ခေါ်ပေးနေပါတယ်... ခဏစောင့်ပါဗျာ။**")

    # ၄။ Member စာရင်းကို ယူမယ်
    members = []
    async for member in client.get_chat_members(chat_id):
        if not member.user.is_bot and not member.user.is_deleted:
            members.append(member.user.mention)

    # ၅။ ၅ ယောက်တစ်တွဲစီ Tag ခေါ်မယ် (Spam မဖြစ်အောင်)
    count = 0
    total_members = len(members)
    
    for i in range(0, total_members, 5):
        # ၅ ယောက်စာ စုမယ်
        chunk = members[i:i+5]
        mention_string = ", ".join(chunk)
        
        # Emoji အလှလေးတွေနဲ့ စာသားကို ပို့မယ်
        try:
            await client.send_message(
                chat_id,
                f"📢 **{custom_message}**\n\n"
                f"✨ {mention_string}\n\n"
                f"💡 စုစုပေါင်း: `{total_members}` ယောက်"
            )
            count += len(chunk)
            await asyncio.sleep(2) # Telegram က Ban မလုပ်အောင် ၂ စက္ကန့်စီ ခြားပြီး ပို့မယ်
        except Exception as e:
            print(f"Tag Error: {e}")
            break

    # ၆။ ပြီးသွားရင် status message ကို ဖျက်မယ်
    await status_msg.edit_text(f"✅ **Member {count} ယောက်လုံးကို Tag ခေါ်ပြီးပါပြီဗျာ!**")
    await asyncio.sleep(5)
    await status_msg.delete()

