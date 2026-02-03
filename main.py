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
LOG_GROUP = int(os.environ.get("LOG_GROUP", "0"))

app = Client("EliteSultan", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
start_time = time.time()

# --- THEME ENGINE (ELITE HTML) ---
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

# --- 1. INTERACTIVE HELP MENU ---
@app.on_message(filters.command("help", ".") & filters.me)
async def help_menu(_, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎯 Trigger", callback_data="mod_trig"), InlineKeyboardButton("🚀 G-Cast", callback_data="mod_gc")],
        [InlineKeyboardButton("🛡 Admin", callback_data="mod_adm"), InlineKeyboardButton("👋 Welcome", callback_data="mod_wel")],
        [InlineKeyboardButton("🛠 Main Features", callback_data="mod_main")]
    ])
    text = elite_html("MENU PENGATURAN", "Silakan pilih modul di bawah untuk melihat penjelasan detail.")
    await message.edit(text, reply_markup=buttons)

@app.on_callback_query()
async def callback_handler(_, query: CallbackQuery):
    data = query.data
    if data == "mod_trig":
        txt = "<b>🎯 TRIGGER</b>\n<blockquote>Respon otomatis grup. Ketik <code>.settrig [kata] [balasan]</code></blockquote>"
    elif data == "mod_gc":
        txt = "<b>🚀 G-CAST / U-CAST</b>\n<blockquote>Broadcast massal ke Grup atau Private Chat.</blockquote>"
    elif data == "mod_adm":
        txt = "<b>🛡 ADMIN ACCESS</b>\n<blockquote>Tambah sudo via <code>.setadmin</code> (reply user).</blockquote>"
    elif data == "mod_wel":
        txt = "<b>👋 WELCOME</b>\n<blockquote>Teks sambutan otomatis member baru.</blockquote>"
    elif data == "mod_main":
        txt = "<b>🛠 MAIN FEATURES</b>\n<blockquote>• .status\n• .steal (Bypass ViewOnce)\n• .tagall\n• .sd (Self Destruct)</blockquote>"
    
    back = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="mod_back")]])
    await query.edit_message_text(elite_html("PENJELASAN MODUL", txt), reply_markup=back if data != "mod_back" else None)
    if data == "mod_back":
        await help_menu(None, query.message)

# --- 2. FITUR STEAL (BYPASS VIEW ONCE) ---
@app.on_message(filters.command("steal", ".") & filters.me)
async def ghost_steal(client, message):
    reply = message.reply_to_message
    if not reply or not reply.media: return await message.delete()
    await message.delete()
    path = await client.download_media(reply)
    cap = elite_html("STEAL RESULT", f"Ditarik dari: {reply.from_user.mention}")
    await client.send_document("me", path, caption=cap)
    if os.path.exists(path): os.remove(path)

# --- 3. G-CAST & U-CAST ---
@app.on_message(filters.command(["gcast", "ucast"], ".") & (filters.me | filters.user(SUDO_USERS)))
async def broadcast_pro(client, message):
    cmd = message.command[0]
    text = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
    if not text: return await message.edit("<code>Pesan kosong!</code>")
    await message.edit(f"<code>🚀 {cmd.upper()} Pro In Progress...</code>")
    count = 0
    target = [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP] if cmd == "gcast" else [enums.ChatType.PRIVATE]
    async for dialog in client.get_dialogs():
        if dialog.chat.type in target:
            try:
                await client.send_message(dialog.chat.id, text)
                count += 1
                await asyncio.sleep(0.3)
            except: continue
    await message.edit(elite_html(f"{cmd.upper()} DONE", f"Terkirim ke <code>{count}</code> chat."))

# --- 4. STATUS & SUDO ---
@app.on_message(filters.command("status", ".") & (filters.me | filters.user(SUDO_USERS)))
async def status_dash(_, message):
    start = datetime.now()
    ping = (datetime.now() - start).microseconds / 1000
    res = f"• <b>Ping :</b> <code>{ping}ms</code>\n• <b>Uptime :</b> <code>{get_uptime()}</code>\n• <b>Admin :</b> <code>{len(SUDO_USERS)}</code>"
    await message.edit(elite_html("ELITE SYSTEM", res))

@app.on_message(filters.command("setadmin", ".") & filters.me)
async def add_sudo(_, message):
    if not message.reply_to_message: return await message.edit("<code>Reply usernya!</code>")
    SUDO_USERS.append(message.reply_to_message.from_user.id)
    await message.edit(elite_html("ADMIN ADDED", f"User <code>{message.reply_to_message.from_user.id}</code> diizinkan."))

# --- 5. TAGALL & SELF DESTRUCT ---
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
    timer = int(message.command[1]); text = " ".join(message.command[2:])
    await message.edit(elite_html("SELF DESTRUCT", f"🕒 {timer}s: {text}"))
    await asyncio.sleep(timer); await message.delete()

app.run()
