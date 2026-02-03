import os
import asyncio
import time
from datetime import datetime
from pyrogram import Client, filters

# --- SETUP ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION")

app = Client("EliteSultan", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
start_time = time.time()

# --- THEME ENGINE (SIMPLE & PINK VIBES) ---
# Menggunakan dot minimalis dan font monospace
def pink_ui(content):
    return (
        f"🌸 <b>𝖤𝗅𝗂𝗍𝖾 𝖲𝗒𝗌𝗍𝖾𝗆</b>\n"
        f"───\n"
        f"<blockquote>{content}</blockquote>\n"
        f"───"
    )

def get_uptime():
    delta = round(time.time() - start_time)
    hours, remainder = divmod(delta, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

# --- 1. STATUS (SIMPLE PINK) ---
@app.on_message(filters.command("status", ".") & filters.me)
async def status_dash(_, message):
    start = datetime.now()
    await message.edit("<code>Processing...</code>")
    end = datetime.now()
    ping = (end - start).microseconds / 1000
    
    res = (
        f"<b>• 𝖯𝗂𝗇𝗀 :</b> <code>{ping}ms</code>\n"
        f"<b>• 𝖴𝗉𝗍𝗂𝗆𝖾 :</b> <code>{get_uptime()}</code>\n"
        f"<b>• 𝖮𝗐𝗇𝖾𝗋 :</b> {message.from_user.mention}\n"
        f"<b>• 𝖱𝖾𝗌𝗎𝗅𝗍 𝖻𝗒 :</b> 𝖤𝗅𝗂𝗍𝖾-𝖷"
    )
    await message.edit(pink_ui(res))

# --- 2. OPTIMAL TAGALL (NO DELAY JEDUG) ---
@app.on_message(filters.command("tagall", ".") & filters.me)
async def tagall_optimal(client, message):
    text = message.text.split(None, 1)[1] if len(message.command) > 1 else "Heads up!"
    await message.delete()
    
    members = []
    async for m in client.get_chat_members(message.chat.id):
        if not m.user.is_bot and not m.user.is_deleted:
            members.append(m.user.mention)
    
    # Tag per 5 orang biar gak spam-limit tapi tetep cepet
    for i in range(0, len(members), 5):
        container = f"✨ {text}\n" + " ".join(members[i:i+5])
        await client.send_message(message.chat.id, container)
        await asyncio.sleep(0.3) # Optimized speed

# --- 3. FIX STEAL (MEDIA BYPASS) ---
@app.on_message(filters.command("steal", ".") & filters.me)
async def steal_fix(client, message):
    if not message.reply_to_message:
        return await message.edit("<code>Balas ke medianya, Bos!</code>")
    
    await message.edit("<code>🔐 Securing media...</code>")
    # Pake copy_message biar bypass view-once lebih aman
    await client.copy_message("me", message.chat.id, message.reply_to_message.id)
    await message.edit("<code>✅ Stored in Saved Messages.</code>")

# --- 4. FIX SELF DESTRUCT (.sd) ---
@app.on_message(filters.command("sd", ".") & filters.me)
async def sd_fix(_, message):
    if len(message.command) < 3:
        return await message.edit("<code>Format: .sd [detik] [teks]</code>")
    
    try:
        timer = int(message.command[1])
        text = " ".join(message.command[2:])
        await message.edit(pink_ui(f"🕒 {timer}𝗌 : {text}"))
        await asyncio.sleep(timer)
        await message.delete()
    except Exception as e:
        await message.edit(f"Error: {e}")

# --- 5. GHOST READ ---
@app.on_message(filters.command("read", ".") & filters.me)
async def read_ghost(client, message):
    if not message.reply_to_message:
        return await message.edit("<code>Reply ke chat orang!</code>")
    
    msg = message.reply_to_message
    content = f"👤 {msg.from_user.first_name}\n💬 {msg.text or '[Media/Sticker]'}"
    await message.edit(pink_ui(content))

print("Elite-X V3 Active...")
app.run()
