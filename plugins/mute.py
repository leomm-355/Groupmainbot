import asyncio
import re
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions


warns = {}

# Link တွေကို စစ်ဆေးဖို့ Regular Expression
LINK_PATTERN = r"(https?://\S+|t\.me/\S+|@\S+)"

@Client.on_message(filters.group & (filters.text | filters.forwarded))
async def auto_mute_handler(client: Client, message: Message):
    
    member = await message.chat.get_member(message.from_user.id)
    if member.status in ["administrator", "creator"]:
        return

    #
    has_link = re.search(LINK_PATTERN, message.text) if message.text else False
    is_forwarded = message.forward_date is not None

    if has_link or is_forwarded:
        user_id = message.from_user.id
        chat_id = message.chat.id
        user_key = f"{chat_id}:{user_id}"

        #
        current_warns = warns.get(user_key, 0) + 1
        warns[user_key] = current_warns

        if current_warns < 3:
            # --- သတိပေးစာ ပို့မယ် ---
            warn_msg = await message.reply_text(
                f"⚠️ {message.from_user.mention}၊  Link များ သို့မဟုတ် Forward များ ပို့ခွင့်မရှိပါ။\n"
                f"သတိပေးချက်: ({current_warns}/3)\n"
                f"၃ ကြိမ်ပြည့်ပါက ၁ မိနစ် Mute ခံရပါမည်။"
            )
            # မက်ဆေ့ခ်ျဟောင်းကို ဖျက်မယ်
            try:
                await message.delete()
            except:
                pass
            
            
            await asyncio.sleep(10)
            await warn_msg.delete()

        else:
            # 
            try:
                # လက်ရှိအချိန် + ၁ မိနစ်
                until_time = int(asyncio.get_event_loop().time()) + 60
                
                await message.chat.restrict_member(
                    user_id,
                    permissions=ChatPermissions(can_send_messages=False),
                    until_date=asyncio.get_event_loop().time() + 60
                )
                
                mute_msg = await message.reply_text(
                    f"🚫 {message.from_user.mention} သည် စည်းကမ်းဖောက်ဖျက်မှု ၃ ကြိမ်ပြည့်သဖြင့် ၁ မိနစ်ခန့် Mute ခံလိုက်ရသည်။"
                )
                
                # Warn counter ကို Reset ပြန်လုပ်မယ်
                warns[user_key] = 0
                
                # 
                try:
                    await message.delete()
                except:
                    pass

                await asyncio.sleep(60)
                await mute_msg.delete()

            except Exception as e:
                print(f"Mute Error: {e}")
