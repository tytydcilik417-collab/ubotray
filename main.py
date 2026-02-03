import os
import asyncio
import time
from datetime import datetime
# BARIS DI BAWAH INI ADALAH OBAT ERROR TADI
from pyrogram import Client, filters 

# --- AMBIL DATA DARI VARIABLE RAILWAY ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION")

app = Client("EliteSultan", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)

# --- THEME ENGINE V3 (ULTRA PREMIUM) ---
def sultan_ui(title, body):
    return (
        f"<b>╔════ {title} ════╗</b>\n"
        f"<b>  💎 𝖲𝖳𝖠𝖳𝖴𝖲:</b> <code>RAY BAIK</code>\n"
        f"<b>  🛡 𝖲𝖤𝖢𝖴𝖱𝖨𝖳𝖸:</b> <code>𝖠𝖢𝖳𝖨𝖵𝖤</code>\n"
        f"<b>╚════════════════════╝</b>\n"
        f"<b>{body}</b>\n"
        f"<b>──────────────</b>"
    )

# --- 1. FITUR STATUS (DASHBOARD MAHAL) ---
@app.on_message(filters.command("status", ".") & filters.me)
async def status_dash(_, message):
    start = datetime.now()
    await message.edit("<code>Connecting to Elite Server...</code>")
    ping = (datetime.now() - start).microseconds / 1000
    res = f"📡 𝖫𝖺𝗍𝖾𝗇𝖼𝗒: <code>{ping}ms</code>\n💎 𝖯𝗅𝖺𝗇: <code>𝖲𝗎𝗅𝗍𝖺𝗇-𝖷</code>\n🛰 𝖲𝖾𝗋𝗏𝖾𝗋: <code>𝖱𝖺𝗂𝗅𝗐𝖺𝗒.𝖺𝗉𝗉</code>"
    await message.edit(sultan_ui("𝖲𝖸𝖲𝖳𝖤𝖬 𝖢𝖧𝖤𝖢𝖪", res))

# --- 2. FITUR TAG ALL (SILENT & FAST) ---
@app.on_message(filters.command("tagall", ".") & filters.me)
async def tagall_sultan(client, message):
    await message.delete()
    chat_id = message.chat.id
    members = []
    async for m in client.get_chat_members(chat_id):
        if not m.user.is_bot: members.append(m.user.mention)
    
    for i in range(0, len(members), 5):
        await client.send_message(chat_id, f"⚡️ RAY 𝖠𝖭𝖭𝖮𝖴𝖢𝖤 ⚡️\n" + " ".join(members[i:i+5]))
        await asyncio.sleep(1)

# --- 3. FITUR STEAL MEDIA (VIEW ONCE BYPASS) ---
@app.on_message(filters.command("steal", ".") & filters.me)
async def steal_cmd(client, message):
    if not message.reply_to_message: return
    await message.edit("<code>📥 Extracting Media...</code>")
    await client.copy_message("me", message.chat.id, message.reply_to_message.id)
    await message.edit("<code>✅ Media Secured in Saved Messages.</code>")

# --- 4. FITUR FAKE PREMIUM LOOK (AUTO APPEND ⚡️) ---
@app.on_message(filters.me & ~filters.command(["status", "tagall", "steal", "read"], "."))
async def premium_effect(_, message):
    if message.text:
        try: 
            # Menghindari pengeditan berulang jika pesan diedit ubot lain
            if not message.text.endswith("⚡️"):
                await message.edit(f"{message.text}  ⚡️")
        except: pass

# --- 5. FITUR GHOST READ (BACA DIAM-DIAM Tanpa Centang) ---
@app.on_message(filters.command("read", ".") & filters.me)
async def ghost_read(client, message):
    if message.reply_to_message:
        msg = message.reply_to_message
        res = f"👤 𝖥𝗋𝗈𝗆: {msg.from_user.first_name}\n💬 𝖬𝗌𝖌: {msg.text}"
        await message.edit(sultan_ui("𝖦𝖧𝖮𝖲𝖳 𝖱𝖤𝖠𝖣𝖤𝖱", res))

# --- 6. AUTO DELETE (SELF DESTRUCT) ---
@app.on_message(filters.command("sd", ".") & filters.me)
async def self_destruct(_, message):
    if len(message.command) < 3:
        return await message.edit("Format: .sd [detik] [teks]")
    timer = int(message.command[1])
    text = " ".join(message.command[2:])
    await message.edit(f"🗑 {text}\n\n(Auto delete in {timer}s)")
    await asyncio.sleep(timer)
    await message.delete()

print("Userbot Sultan is Running...")
app.run()

