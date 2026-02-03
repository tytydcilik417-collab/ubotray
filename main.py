import os
import asyncio
import time
from datetime import datetime
from pyrogram import Client, filters, enums

# --- CONFIG ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION")
# Ambil ID Sudo dari Variable Railway (Key: SUDO)
SUDO_USERS = [int(x) for x in os.environ.get("SUDO", "").split()] if os.environ.get("SUDO") else []

app = Client(
    "EliteSultan", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    session_string=SESSION,
    parse_mode=enums.ParseMode.HTML
)

start_time = time.time()

# --- THEME ENGINE (PASTI KUTIP) ---
def elite_html(title, body):
    return (
        f"<b>🌸 {title}</b>\n"
        f"<blockquote>{body}</blockquote>\n"
        f"<i>Result by Elite-X</i>"
    )

def get_uptime():
    delta = round(time.time() - start_time)
    hours, remainder = divmod(delta, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

# --- 1. STATUS (FULL AESTHETIC HTML) ---
@app.on_message(filters.command("status", ".") & (filters.me | filters.user(SUDO_USERS)))
async def status_dash(_, message):
    start = datetime.now()
    ping = (datetime.now() - start).microseconds / 1000
    res = (
        f"• <b>Ping :</b> <code>{ping}ms</code>\n"
        f"• <b>Uptime :</b> <code>{get_uptime()}</code>\n"
        f"• <b>Sudo :</b> <code>{len(SUDO_USERS)} Active</code>"
    )
    await message.edit(elite_html("SYSTEM CHECK", res))

# --- 2. G-CAST & U-CAST (MODUL BROADCAST) ---
@app.on_message(filters.command(["gcast", "ucast"], ".") & (filters.me | filters.user(SUDO_USERS)))
async def broadcast_handler(client, message):
    cmd = message.command[0]
    text = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
    if not text: return await message.edit("<code>Pesan mana yang mau disebar?</code>")
    
    await message.edit(f"<b>🚀 {cmd.upper()} Pro In Progress...</b>")
    count = 0
    target_type = [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP] if cmd == "gcast" else [enums.ChatType.PRIVATE]
    
    async for dialog in client.get_dialogs():
        if dialog.chat.type in target_type:
            try:
                await client.send_message(dialog.chat.id, text)
                count += 1
                await asyncio.sleep(0.3)
            except: continue
    await message.edit(elite_html(f"{cmd.upper()} SUCCESS", f"Berhasil sebar ke <code>{count}</code> chat."))

# --- 3. STEAL (VIEW ONCE BYPASS) ---
@app.on_message(filters.command("steal", ".") & filters.me)
async def ghost_steal(client, message):
    reply = message.reply_to_message
    if not reply or not reply.media: return await message.delete()
    await message.delete()
    try:
        path = await client.download_media(reply)
        caption = elite_html("STEAL RESULT", f"Dari: {reply.from_user.mention}")
        await client.send_document("me", path, caption=caption)
        if os.path.exists(path): os.remove(path)
    except: pass

# --- 4. TAGALL ---
@app.on_message(filters.command("tagall", ".") & filters.me)
async def tag_all(client, message):
    note = " ".join(message.command[1:]) if len(message.command) > 1 else "Woi!"
    await message.delete()
    mems = [m.user.mention async for m in client.get_chat_members(message.chat.id) if not m.user.is_bot]
    for i in range(0, len(mems), 5):
        await client.send_message(message.chat.id, f"✨ <b>{note}</b>\n" + " ".join(mems[i:i+5]))
        await asyncio.sleep(0.3)

# --- 5. SELF DESTRUCT (.sd) ---
@app.on_message(filters.command("sd", ".") & filters.me)
async def self_dest(client, message):
    if len(message.command) < 3: return
    timer = int(message.command[1]); text = " ".join(message.command[2:])
    await message.edit(elite_html("SELF DESTRUCT", f"🕒 {timer}s: {text}"))
    await asyncio.sleep(timer); await message.delete()

# --- 6. HELP MENU ---
@app.on_message(filters.command("help", ".") & filters.me)
async def help_cmd(_, message):
    help_text = (
        "<b>🌸 ELITE-X MODULES</b>\n"
        "• <code>.status</code> - Cek Sistem\n"
        "• <code>.gcast</code> - Broadcast Grup\n"
        "• <code>.ucast</code> - Broadcast Private\n"
        "• <code>.steal</code> - Maling ViewOnce\n"
        "• <code>.tagall</code> - Tag Member\n"
        "• <code>.sd</code> - Self Destruct"
    )
    await message.edit(elite_html("DAFTAR MODUL", help_text))

app.run()
