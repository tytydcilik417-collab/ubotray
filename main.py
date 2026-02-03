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

# --- THEME ENGINE (PINK MINIMALIST) ---
def pink_ui(content):
    return (
        f"🌸 <b>𝖤𝗅𝗂𝗍𝖾 𝖲𝗒𝗌𝗍𝖾𝗆</b>\n"
        f"<blockquote>{content}</blockquote>"
    )

def get_uptime():
    delta = round(time.time() - start_time)
    hours, remainder = divmod(delta, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

# --- 1. STATUS (SIMPLE & ELEGANT) ---
@app.on_message(filters.command("status", ".") & filters.me)
async def status_dash(_, message):
    start = datetime.now()
    ping = (datetime.now() - start).microseconds / 1000
    res = (
        f"<b>• 𝖯𝗂𝗇𝗀 :</b> <code>{ping}ms</code>\n"
        f"<b>• 𝖴𝗉𝗍𝗂𝗆𝖾 :</b> <code>{get_uptime()}</code>\n"
        f"<b>• 𝖮w𝗇𝖾𝗋 :</b> {message.from_user.mention}\n"
        f"<b>• 𝖱𝖾𝗌𝗎𝗅𝗍 𝖻𝗒 :</b> 𝖤𝗅𝗂𝗍𝖾-𝖷"
    )
    await message.edit(pink_ui(res))

# --- 2. OPTIMIZED TAGALL ---
@app.on_message(filters.command("tagall", ".") & filters.me)
async def tagall_optimal(client, message):
    args = message.text.split(None, 1)[1] if len(message.command) > 1 else "Heads up!"
    await message.delete()
    members = []
    async for m in client.get_chat_members(message.chat.id):
        if not m.user.is_bot and not m.user.is_deleted:
            members.append(m.user.mention)
    for i in range(0, len(members), 5):
        await client.send_message(message.chat.id, f"✨ {args}\n" + " ".join(members[i:i+5]))
        await asyncio.sleep(0.3)

# --- 3. HARD STEAL (DOWNLOAD & UPLOAD METHOD) ---
# Fitur ini lebih kuat, bisa tembus media yang dilarang copy
@app.on_message(filters.command("steal", ".") & filters.me)
async def steal_hard(client, message):
    reply = message.reply_to_message
    if not reply or not reply.media:
        return await message.edit("<code>Balas ke media!</code>")
    
    await message.edit("<code>📥 Downloading...</code>")
    file_path = await client.download_media(reply)
    await message.edit("<code>📤 Uploading to Cloud...</code>")
    await client.send_document("me", file_path, caption=f"🌸 𝖲𝗍𝖾𝖺𝗅 𝖱𝖾𝗌𝗎𝗅𝗍\n👤 𝖥𝗋𝗈𝗆: {reply.from_user.mention if reply.from_user else 'Unknown'}")
    
    if os.path.exists(file_path):
        os.remove(file_path) # Hapus file di server biar gak penuh
    await message.edit("<code>✅ Secured in Saved Messages.</code>")

# --- 4. SELF DESTRUCT (.sd) ---
@app.on_message(filters.command("sd", ".") & filters.me)
async def sd_fix(_, message):
    if len(message.command) < 3:
        return await message.edit("<code>Format: .sd [detik] [teks]</code>")
    timer = int(message.command[1])
    text = " ".join(message.command[2:])
    await message.edit(pink_ui(f"🕒 {timer}𝗌 : {text}"))
    await asyncio.sleep(timer)
    await message.delete()

# --- 5. GHOST READ ---
@app.on_message(filters.command("read", ".") & filters.me)
async def read_ghost(client, message):
    reply = message.reply_to_message
    if not reply: return await message.edit("<code>Reply ke chat!</code>")
    content = f"👤 {reply.from_user.first_name if reply.from_user else 'User'}\n💬 {reply.text or '[Media]'}"
    await message.edit(pink_ui(content))

print("Elite-X V4 Berhasil Dijalankan!")
app.run()
