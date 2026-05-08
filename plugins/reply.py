import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from bot import db 

# Database Collection
replies = db["auto_replies"]

# Railway Variable ထဲက OWNER_ID ကို ယူမယ် (မရှိရင် 0 လို့ ထားမယ်)
OWNER_ID = int(os.environ.get("OWNER_ID", 0))

@Client.on_message(filters.group & ~filters.bot)
async def auto_learn_and_reply(client: Client, message: Message):
    # --- ၁။ Auto Learning (Global - အကုန်လုံးအတွက် မှတ်မယ်) ---
    if message.reply_to_message:
        reply_to = message.reply_to_message
        
        trigger = None
        trigger_type = None
        
        if reply_to.text:
            trigger = reply_to.text.lower().strip()
            trigger_type = "text"
        elif reply_to.sticker:
            trigger = reply_to.sticker.file_unique_id
            trigger_type = "sticker"

        reply_data = None
        reply_type = None
        
        if message.text:
            reply_data = message.text
            reply_type = "text"
        elif message.sticker:
            reply_data = message.sticker.file_id
            reply_type = "sticker"

        if trigger and reply_data:
            # chat_id မပါဘဲ စစ်တဲ့အတွက် Group အားလုံးအတွက် တစ်ခုပဲ မှတ်ပါမယ်
            exists = await replies.find_one({"trigger": trigger})
            if not exists:
                await replies.insert_one({
                    "trigger": trigger,
                    "trigger_type": trigger_type,
                    "reply": reply_data,
                    "reply_type": reply_type
                })

    # --- ၂။ Auto Reply (ဘယ် Group မှာမဆို ပြန်ဖြေမယ်) ---
    else:
        current_trigger = None
        if message.text:
            current_trigger = message.text.lower().strip()
        elif message.sticker:
            current_trigger = message.sticker.file_unique_id

        if current_trigger:
            found = await replies.find_one({"trigger": current_trigger})
            if found:
                if found["reply_type"] == "text":
                    await message.reply_text(found["reply"])
                else:
                    await message.reply_sticker(found["reply"])

# --- ၃။ Delete Command (Owner သီးသန့်) ---
@Client.on_message(filters.command("del"))
async def delete_reply(client: Client, message: Message):
    # Owner စစ်ဆေးခြင်း
    if message.from_user.id != OWNER_ID:
        return 

    if not message.reply_to_message:
        return await message.reply_text("❌ ဖျက်ချင်တဲ့ အမေးစာကို Reply ပြန်ပြီး `/del` လို့ ရိုက်ပါ။")

    reply_to = message.reply_to_message
    trigger_to_del = None
    
    if reply_to.text:
        trigger_to_del = reply_to.text.lower().strip()
    elif reply_to.sticker:
        trigger_to_del = reply_to.sticker.file_unique_id

    if trigger_to_del:
        # Global ဖြစ်တဲ့အတွက် ဒီ trigger နဲ့ ဆိုင်သမျှ အကုန်ဖျက်မယ်
        result = await replies.delete_many({"trigger": trigger_to_del})
        if result.deleted_count > 0:
            await message.reply_text(f"🗑️ အမေးစာ '{trigger_to_del}' အတွက် အဖြေကို Global Database ထဲက ဖျက်လိုက်ပါပြီ။")
        else:
            await message.reply_text("❌ ဒီစာသားအတွက် မှတ်ထားတဲ့ အဖြေမရှိပါဘူး။")
