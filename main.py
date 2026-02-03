import os
import asyncio
import time
from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- CONFIG ---
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
SESSION = os.environ.get("SESSION", "")

app = Client(
    "EliteSultan", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    session_string=SESSION,
    parse_mode=enums.ParseMode.HTML
)

start_time = time.time()

# --- THEME ENGINE ---
def sepuh_ui(title, body):
    return (
        f"<b>┌── ⌈ {title} ⌋</b>\n"
        f"<blockquote expandable>{body}</blockquote>\n"
        f"<b>└──────────────❑</b>"
    )

def get_uptime():
    delta = round(time.time() - start_time)
    hours, remainder = divmod(delta, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

# --- FITUR SELF DESTRUCT (.sd) ---
@app.on_message(filters.command("sd", ".") & filters.me)
async def self_destruct_sepuh(client, message):
    if len(message.command) < 3:
        return await message.edit("<b>Format:</b> <code>.sd [detik] [teks]</code>\nContoh: <code>.sd 5 lu bau</code>")
    
    try:
        timer = int(message.command[1])
        teks = message.text.split(None, 2)[2]
        
        # Edit pesan jadi teks yang mau dikirim
        await message.edit(teks)
        
        # Tunggu sesuai detik
        await asyncio.sleep(timer)
        
        # Hapus pesan
        await message.delete()
        
    except ValueError:
        await message.edit("<code>Input detik harus angka, sepuh!</code>")
    except Exception as e:
        await message.edit(f"<b>Error:</b> <code>{e}</code>")

# --- FITUR STEAL (BYPASS VIEW ONCE) ---
@app.on_message(filters.command("steal", ".") & filters.me)
async def steal_sepuh(client, message):
    reply = message.reply_to_message
    if not reply or not reply.media:
        return await message.edit("<code>Balas ke foto/video sekali lihat!</code>")
    
    await message.edit("<code>Mencuri media... ⚡</code>")
    try:
        # Download media
        path = await client.download_media(reply)
        
        # Kirim ke Saved Messages (me)
        await client.send_document(
            "me", 
            path, 
            caption=sepuh_ui("STEAL SUCCESS", f"<b>Dari:</b> {reply.from_user.first_name if reply.from_user else 'Secret'}")
        )
        
        await message.edit("<code>Media aman di Saved Messages!</code>")
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        await message.edit(f"<b>Gagal steal:</b> <code>{e}</code>")

# --- FITUR STATUS ---
@app.on_message(filters.command("status", ".") & filters.me)
async def status_sepuh(_, message):
    start = datetime.now()
    ping = (datetime.now() - start).microseconds / 1000
    content = (
        f"<b>Ping:</b> <code>{ping}ms</code>\n"
        f"<b>Uptime:</b> <code>{get_uptime()}</code>\n"
        f"<b>Engine:</b> <code>Elite-X Premium</code>"
    )
    await message.edit(sepuh_ui("SYSTEM STATUS", content))

# --- FITUR HELP (DENGAN TOMBOL) ---
@app.on_message(filters.command("help", ".") & filters.me)
async def help_sepuh(_, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛠 Modul", callback_data="mod_trig"), InlineKeyboardButton("🏠 Menu", callback_data="mod_main")],
        [InlineKeyboardButton("🗑 Close", callback_data="close_menu")]
    ])
    
    content = (
        "<b>• .sd:</b> Pesan hapus otomatis.\n"
        "<b>• .steal:</b> Ambil media sekali lihat.\n"
        "<b>• .status:</b> Info bot (Kutip ciut).\n"
        "<b>• .tagall:</b> Tag semua member grup."
    )
    
    try:
        await message.edit(sepuh_ui("MENU ELITE", content), reply_markup=buttons)
    except:
        await message.edit(sepuh_ui("MENU ELITE", content))

app.run()
