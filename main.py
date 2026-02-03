import os
import asyncio
import time
from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- CONFIG ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION")

app = Client(
    "EliteSultan", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    session_string=SESSION,
    parse_mode=enums.ParseMode.HTML
)

start_time = time.time()

# --- THEME ENGINE (REAL SEPUH QUOTE) ---
def sepuh_ui(title, body):
    # Menggunakan kombinasi garis dekorasi dan blockquote agar mirip SS
    return (
        f"<b>┌── ⌈ {title} ⌋ ──❑</b>\n"
        f"<blockquote>{body}</blockquote>\n"
        f"<b>└──────────────❑</b>"
    )

def get_uptime():
    delta = round(time.time() - start_time)
    hours, remainder = divmod(delta, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

# --- FITUR STATUS (MIRIP SS) ---
@app.on_message(filters.command("status", ".") & filters.me)
async def status_sepuh(_, message):
    start = datetime.now()
    ping = (datetime.now() - start).microseconds / 1000
    
    # Body menggunakan simbol list agar rapi
    content = (
        f"┣ 🏓 <b>Ping:</b> <code>{ping}ms</code>\n"
        f"┣ ⏰ <b>Uptime:</b> <code>{get_uptime()}</code>\n"
        f"┣ 👤 <b>Owner:</b> {message.from_user.mention}\n"
        f"┗ 🤖 <b>Result By:</b> <code>Elite-X</code>"
    )
    await message.edit(sepuh_ui("INFO STATUS", content))

# --- FITUR HELP (MENU PENGATURAN) ---
@app.on_message(filters.command("help", ".") & filters.me)
async def help_sepuh(_, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("👈 Trigger", callback_data="mod_trig"), InlineKeyboardButton("🏠 Menu Utama", callback_data="mod_main")]
    ])
    
    # Teks isi menu sesuai SS yang lo mau
    content = (
        "<b>• Trigger:</b> Respon otomatis grup.\n"
        "<b>• Tombol:</b> Link menu start.\n"
        "<b>• Media:</b> Foto/Video menu utama.\n"
        "<b>• Teks:</b> Sambutan menu utama.\n"
        "<b>• Admin:</b> Tambah akses admin bot."
    )
    await message.edit(sepuh_ui("MENU PENGATURAN", content), reply_markup=buttons)

# --- FITUR STEAL (BYPASS) ---
@app.on_message(filters.command("steal", ".") & filters.me)
async def steal_sepuh(client, message):
    reply = message.reply_to_message
    if not reply or not reply.media: return await message.delete()
    await message.delete()
    path = await client.download_media(reply)
    await client.send_document("me", path, caption=sepuh_ui("STEAL SUCCESS", f"Owner: {reply.from_user.first_name}"))
    if os.path.exists(path): os.remove(path)

# --- FITUR TAGALL ---
@app.on_message(filters.command("tagall", ".") & filters.me)
async def tagall_sepuh(client, message):
    await message.delete()
    mems = [m.user.mention async for m in client.get_chat_members(message.chat.id) if not m.user.is_bot]
    for i in range(0, len(mems), 5):
        await client.send_message(message.chat.id, f"📢 <b>Tag All!</b>\n" + " ".join(mems[i:i+5]))
        await asyncio.sleep(0.3)

app.run()
