import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("couple") & filters.group)
async def couple_handler(client, message):
    chat_id = message.chat.id
    
    # ခေတ္တစောင့်ရန် အကြောင်းကြားမယ်
    status_msg = await message.reply_text("🔍 ဒီနေ့အတွက် အတွဲလေးကို ရှာဖွေပေးနေပါတယ်...")

    # Member စာရင်းကို ယူမယ်
    members = []
    try:
        async for member in client.get_chat_members(chat_id):
            if not member.user.is_bot and not member.user.is_deleted:
                members.append(member.user.mention)
    except Exception as e:
        return await status_msg.edit_text("❌ Member စာရင်းကို ယူလို့မရပါဘူး။ Bot ကို Admin ပေးထားဖို့ လိုပါမယ်။")

    if len(members) < 2:
        return await status_msg.edit_text("❌ ဒီ Group မှာ လူနည်းလွန်းလို့ အတွဲရွေးလို့ မရသေးပါဘူး။")

    # လူနှစ်ယောက်ကို ကျပန်း ရွေးမယ်
    chosen_ones = random.sample(members, 2)
    c1, c2 = chosen_ones[0], chosen_ones[1]

    couple_text = (
        f"💌 **ဒီနေ့ရဲ့ ကံအကောင်းဆုံး အတွဲလေးကတော့...**\n\n"
        f"{c1}  💖  {c2}\n\n"
        f"💞 ဆုတောင်းစာ 💞\n"
        f"တစ်ယောက်ကိုတစ်ယောက် အပြန်အလှန် နားလည်မှုရှိရှိနဲ့ "
        f"ချစ်ခြင်းမေတ္တာတွေ ထာဝရ တည်မြဲပါစေကြောင်း ဆုတောင်းပေးလိုက်ပါတယ်ဗျာ။ ✨"
    )
    
    # Button ထည့်မယ်
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("သင့် Group မှာလည်း Add လိုက်ပါ ➕", url=f"https://t.me/{client.me.username}?startgroup=true")
        ]
    ])
    
    await status_msg.edit_text(couple_text, reply_markup=buttons)

# --- အသုံးပြုပုံ (Help Message) ---
@Client.on_message(filters.command("couple") & ~filters.group)
async def couple_help(client, message):
    help_text = (
        "👫 **Couple Finder အသုံးပြုနည်း**\n\n"
        "ဒီ Command ကို Group ထဲမှာပဲ သုံးလို့ရပါတယ်ဗျာ။\n\n"
        "✅ `/couple` လို့ ရိုက်လိုက်ရင် Group ထဲက Member တွေထဲကနေ "
        "အတွဲတစ်တွဲကို Bot က ကျပန်း (Random) ရွေးချယ်ပေးမှာ ဖြစ်ပါတယ်။"
    )
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Group ထဲသို့ ထည့်ရန် ➕", url=f"https://t.me/{client.me.username}?startgroup=true")
        ]
    ])
    
    await message.reply_text(help_text, reply_markup=buttons)
