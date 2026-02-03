import os
import asyncio
import time
from datetime import datetime
from pyrogram import Client, filters

# --- CONFIG ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION")

app = Client("EliteSultan", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
start_time = time.time()

def get_uptime():
    delta = round(time.time() - start_time)
    hours, remainder = divmod(delta, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

# --- 1. STATUS (ESTETIK QUOTE PINK) ---
@app.on_message(filters.command("status", ".") & filters.me)
async def status_dash(_, message):
    start = datetime.now()
    ping = (datetime.now() - start).microseconds / 1000
    # Desain Quote Estetik
    res = (
        f"**> 🌸 𝖤𝗅𝗂𝗍𝖾 𝖲𝗒𝗌𝗍𝖾𝗆 𝖠𝖼𝗍𝗂𝗏𝖾**\n"
        f"**>**\n"
        f"**> • 𝖯𝗂𝗇𝗀 :** `{ping}ms`\n"
        f"**> • 𝖴𝗉𝗍𝗂𝗆𝖾 :** `{get_uptime()}`\n"
        f"**> • 𝖮𝗐𝗇𝖾𝗋 :** {message.from_user.mention}\n"
        f"**> • 𝖱𝖾𝗌𝗎𝗅𝗍 𝖻𝗒 :** 𝖤𝗅𝗂𝗍𝖾-𝖷"
    )
    await message.edit(res)

# --- 2. THE GHOST STEAL (VIEW ONCE BYPASS) ---
@app.on_message(filters.command("steal", ".") & filters.me)
async def ghost_steal(client, message):
    reply = message.reply_to_message
    if not reply or not reply.media:
        await message.edit("`❌ Balas ke medianya!`")
        await asyncio.sleep(3)
        return await message.delete()
    
    # Hapus jejak perintah
    await message.delete()
    
    try:
        # Proses Download
        file_path = await client.download_media(reply)
        
        # Kirim ke Saved Messages
        caption = (
            f"🌸 **𝖲𝗍𝖾𝖺𝗅 𝖱𝖾𝗌𝗎𝗅𝗍**\n\n"
            f"**> 𝖥𝗋𝗈𝗆 :** {reply.from_user.mention if reply.from_user else '𝖴𝗇𝗄𝗇𝗈𝗐𝗇'}\n"
            f"**> 𝖢𝗁𝖺𝗍 :** `{message.chat.title or '𝖯𝗋𝗂𝗏𝖺𝗍𝖾'}`"
        )
        
        await client.send_document("me", file_path, caption=caption)
        
        # Bersihkan file sampah
        if os.path.exists(file_path):
            os.remove(file_path)
            
    except Exception as e:
        await client.send_message("me", f"❌ **𝖦𝖺𝗀𝖺𝗅 𝖬𝖺𝗅𝗂𝗇𝗀:** `{e}`")

# --- 3. OPTIMIZED TAGALL ---
@app.on_message(filters.command("tagall", ".") & filters.me)
async def tagall_optimal(client, message):
    args = message.text.split(None, 1)[1] if len(message.command) > 1 else "𝖧𝖾𝖺𝖽𝗌 𝗎𝗉!"
    await message.delete()
    members = []
    async for m in client.get_chat_members(message.chat.id):
        if not m.user.is_bot and not m.user.is_deleted:
            members.append(m.user.mention)
    
    for i in range(0, len(members), 5):
        await client.send_message(message.chat.id, f"✨ {args}\n" + " ".join(members[i:i+5]))
        await asyncio.sleep(0.3)

# --- 4. SELF DESTRUCT (.sd) ---
@app.on_message(filters.command("sd", ".") & filters.me)
async def sd_fix(_, message):
    if len(message.command) < 3:
        await message.edit("`Format: .sd [detik] [teks]`")
        await asyncio.sleep(3)
        return await message.delete()
        
    try:
        timer = int(message.command[1])
        text = " ".join(message.command[2:])
        await message.edit(f"**> 🕒 {timer}𝗌 : {text}**")
        await asyncio.sleep(timer)
        await message.delete()
    except:
        await message.delete()

print("Elite-X V6 is Live!")
app.run()
