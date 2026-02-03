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

# --- THEME ENGINE ---
def sepuh_ui(title, body):
    # Menggunakan blockquote (model kutipan Telegram)
    return (
        f"<b>┌── ⌈ {title} ⌋ ──❑</b>\n"
        f"<blockquote>{body}</blockquote>\n"
        f"<b>└──────────────❑</b>"
    )

def get_uptime():
    delta = round(time.time() - start_time)
    hours, remainder = divmod(delta, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}j {minutes}m {seconds}d"

# --- FITUR STATUS ---
@app.on_message(filters.command("status", ".") & filters.me)
async def status_sepuh(_, message):
    start = datetime.now()
    ping = (datetime.now() - start).microseconds / 1000
    
    content = (
        f"🏓 <b>Ping:</b> <code>{ping}ms</code>\n"
        f"⏰ <b>Uptime:</b> <code>{get_uptime()}</code>\n"
        f"👤 <b>Owner:</b> {message.from_user.mention}\n"
        f"⚙️ <b>Engine:</b> <code>Elite-X v2.0</code>"
    )
    # Tampilan status menggunakan model kutipan
    await message.edit(sepuh_ui("SYSTEM STATUS", content))

# --- FITUR HELP DENGAN TOMBOL ---
@app.on_message(filters.command("help", ".") & filters.me)
async def help_sepuh(_, message):
    # Note: Tombol Inline hanya berfungsi jika Userbot ini memiliki akses bot token/bot mode
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🛠 Fitur", callback_data="help_tools"),
            InlineKeyboardButton("👑 Admin", callback_data="help_admin")
        ],
        [InlineKeyboardButton("🌐 Support Group", url="https://t.me/your_group")]
    ])
    
    content = (
        "<b>Daftar Modul Tersedia:</b>\n\n"
        "• <code>.status</code> - Cek performa bot\n"
        "• <code>.steal</code> - Ambil media (Reply)\n"
        "• <code>.tagall</code> - Tag semua member\n"
        "• <code>.help</code> - Menu bantuan ini"
    )
    
    try:
        await message.edit(
            sepuh_ui("ELITE-X MENU", content),
            reply_markup=buttons
        )
    except Exception:
        # Userbot biasa kadang tidak bisa kirim inline keyboard di chat publik/private orang lain
        await message.edit(sepuh_ui("ELITE-X MENU", content + "\n\n<i>(Button unsupported in this chat)</i>"))

# --- FITUR STEAL (BYPASS VIEW ONCE) ---
@app.on_message(filters.command("steal", ".") & filters.me)
async def steal_sepuh(client, message):
    reply = message.reply_to_message
    
    if not reply:
        return await message.edit("<code>Balas ke foto/video sekali lihat!</code>")

    # Cek apakah itu media
    if not reply.media:
        return await message.edit("<code>Media tidak ditemukan.</code>")

    await message.edit("<code>Sedang mencuri media... 🤫</code>")
    
    try:
        # Download media ke memory/file
        file_path = await client.download_media(reply)
        
        # Kirim ke Saved Messages (me)
        caption = f"✅ <b>Steal Berhasil!</b>\n👤 <b>Dari:</b> {reply.from_user.mention if reply.from_user else 'Unknown'}"
        
        # Kirim balik sebagai dokumen/foto biasa agar tidak hilang
        await client.send_document(
            "me", 
            file_path, 
            caption=sepuh_ui("STEAL LOG", caption)
        )
        
        await message.edit("<code>Media tersimpan di Saved Messages!</code>")
        
        # Hapus file setelah dikirim
        if os.path.exists(file_path):
            os.remove(file_path)
            
    except Exception as e:
        await message.edit(f"<b>Gagal steal:</b> <code>{e}</code>")

# --- FITUR TAGALL ---
@app.on_message(filters.command("tagall", ".") & filters.me)
async def tagall_sepuh(client, message):
    await message.delete()
    chat_id = message.chat.id
    
    # Ambil semua member
    members = []
    async for member in client.get_chat_members(chat_id):
        if not member.user.is_bot and not member.user.is_deleted:
            members.append(member.user.mention)
    
    # Kirim tag per 5 orang agar tidak spam berlebihan
    for i in range(0, len(members), 5):
        text = "📢 <b>Panggilan Sepuh!</b>\n\n" + " ".join(members[i:i+5])
        await client.send_message(chat_id, text)
        await asyncio.sleep(0.5)

print("Userbot Berhasil Dijalankan!")
app.run()
