import os
import asyncio
import time
from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# --- CONFIG ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION")
SUDO_USERS = [int(x) for x in os.environ.get("SUDO", "").split()] if os.environ.get("SUDO") else []

# Inisialisasi Database Sederhana untuk Trigger
triggers = {}

app = Client("EliteSultan", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
start_time = time.time()

# --- THEME ENGINE (FIXED HTML QUOTE) ---
def elite_html(title, body):
    # Menggunakan parse_mode=HTML adalah kunci kotak transparan
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

# --- 1. MODUL TRIGGER (Fungsional) ---
@app.on_message(filters.command("settrig", ".") & filters.me)
async def set_trigger(_, message):
    if len(message.command) < 3:
        return await message.edit("<code>Format: .settrig [kata] [balasan]</code>")
    key = message.command[1].lower()
    val = " ".join(message.command[2:])
    triggers[key] = val
    await message.edit(elite_html("TRIGGER SET", f"Kata kunci <code>{key}</code> berhasil disimpan!"))

@app.on_message(filters.text & ~filters.me & filters.group)
async def trigger_handler(_, message):
    text = message.text.lower()
    if text in triggers:
        await message.reply(triggers[text])

# --- 2. STATUS (FULL QUOTE HTML) ---
@app.on_message(filters.command("status", ".") & (filters.me | filters.user(SUDO_USERS)))
async def status_dash(_, message):
    start = datetime.now()
    ping = (datetime.now() - start).microseconds / 1000
    res = (
        f"• <b>Ping :</b> <code>{ping}ms</code>\n"
        f"• <b>Uptime :</b> <code>{get_uptime()}</code>\n"
        f"• <b>Admin :</b> <code>{len(SUDO_USERS)}</code>\n"
        f"• <b>Triggers :</b> <code>{len(triggers)}</code>"
    )
    # Pakai parse_mode HTML agar <blockquote> muncul
    await message.edit(elite_html("ELITE SYSTEM", res), parse_mode=enums.ParseMode.HTML)

# --- 3. HELP MENU (BUTTON INTERAKTIF) ---
@app.on_message(filters.command("help", ".") & filters.me)
async def help_menu(_, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎯 Modul", callback_data="view_mods"), InlineKeyboardButton("🛠 Fitur", callback_data="view_feats")],
        [InlineKeyboardButton("🏠 Menu Utama", callback_data="view_home")]
    ])
    await message.edit(elite_html("MENU PENGATURAN", "Klik tombol di bawah untuk akses modul."), reply_markup=buttons, parse_mode=enums.ParseMode.HTML)

@app.on_callback_query()
async def callback_handler(_, query: CallbackQuery):
    if query.data == "view_mods":
        txt = "<b>MODUL AKTIF:</b>\n1. <b>Trigger:</b> <code>.settrig</code>\n2. <b>Admin:</b> <code>.setadmin</code>\n3. <b>Gcast:</b> <code>.gcast</code>"
    elif query.data == "view_feats":
        txt = "<b>FITUR UTAMA:</b>\n• <code>.steal</code> (Maling Media)\n• <code>.tagall</code> (Tag Member)\n• <code>.sd</code> (Hapus Pesan)"
    else:
        txt = "Pilih modul sultan lo di bawah ini."
    
    await query.edit_message_text(elite_html("DASHBOARD", txt), parse_mode=enums.ParseMode.HTML)

# --- 4. GHOST STEAL (VIEW ONCE) ---
@app.on_message(filters.command("steal", ".") & filters.me)
async def ghost_steal(client, message):
    reply = message.reply_to_message
    if not reply or not reply.media: return await message.delete()
    await message.delete()
    path = await client.download_media(reply)
    await client.send_document("me", path, caption=elite_html("STEAL", f"From: {reply.from_user.first_name}"))
    if os.path.exists(path): os.remove(path)

# --- 5. TAGALL & SD ---
@app.on_message(filters.command("tagall", ".") & filters.me)
async def tag_all(client, message):
    note = " ".join(message.command[1:]) if len(message.command) > 1 else "Woi!"
    await message.delete()
    mems = [m.user.mention async for m in client.get_chat_members(message.chat.id) if not m.user.is_bot]
    for i in range(0, len(mems), 5):
        await client.send_message(message.chat.id, f"✨ <b>{note}</b>\n" + " ".join(mems[i:i+5]))
        await asyncio.sleep(0.3)

@app.on_message(filters.command("sd", ".") & filters.me)
async def self_dest(client, message):
    if len(message.command) < 3: return
    timer = int(message.command[1]); text = " ".join(message.command[2:])
    await message.edit(elite_html("SELF DESTRUCT", f"🕒 {timer}s: {text}"), parse_mode=enums.ParseMode.HTML)
    await asyncio.sleep(timer); await message.delete()

print("Elite-X V11 Ready!")
app.run()
