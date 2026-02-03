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

# --- THEME ENGINE (EXPANDABLE QUOTE) ---
def sepuh_ui(title, body):
    # Menggunakan 'expandable' agar kutipan bisa diklik/diciutkan
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

# --- FITUR STATUS (MODEL KUTIPAN CIUT) ---
@app.on_message(filters.command("status", ".") & filters.me)
async def status_sepuh(_, message):
    start = datetime.now()
    ping = (datetime.now() - start).microseconds / 1000
    
    content = (
        f"<b>Ping:</b> <code>{ping}ms</code>\n"
        f"<b>Uptime:</b> <code>{get_uptime()}</code>\n"
        f"<b>Owner:</b> {message.from_user.mention}\n"
        f"<b>Engine:</b> <code>Elite-X Premium</code>\n"
        f"<b>Status:</b> <code>Online & Secure</code>"
    )
    # Output akan masuk dalam box yang bisa diciutkan
    await message.edit(sepuh_ui("SYSTEM STATUS", content))

# --- FITUR HELP (DENGAN TOMBOL) ---
@app.on_message(filters.command("help", ".") & filters.me)
async def help_sepuh(_, message):
    # Note: Tombol muncul jika akun digunakan sebagai Bot atau via Bot API
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🛠 Modul", callback_data="mod_trig"),
            InlineKeyboardButton("🏠 Menu Utama", callback_data="mod_main")
        ],
        [InlineKeyboardButton("💬 Support Group", url="https://t.me/your_group")]
    ])
    
    content = (
        "<b>• Trigger:</b> Respon otomatis grup.\n"
        "<b>• Tombol:</b> Link menu start.\n"
        "<b>• Media:</b> Foto/Video menu utama.\n"
        "<b>• Teks:</b> Sambutan menu utama.\n"
        "<b>• Admin:</b> Tambah akses admin bot."
    )
    
    try:
        await message.edit(
            sepuh_ui("MENU PENGATURAN", content),
            reply_markup=buttons
        )
    except Exception:
        # Jika userbot biasa, tombol dikirim sebagai teks link di bawahnya
        await message.edit(sepuh_ui("MENU PENGATURAN", content + "\n\n🔗 <b>Menu Utama:</b> t.me/BotLo"))

# --- FITUR STEAL (BYPASS ONCE) ---
@app.on_message(filters.command("steal", ".") & filters.me)
async def steal_sepuh(client, message):
    reply = message.reply_to_message
    if not reply or not reply.media:
        return await message.edit("<code>Balas ke foto/video (sekali lihat)!</code>")
    
    await message.edit("<code>Processing...</code>")
    
    try:
        # Download media yang di-reply
        path = await client.download_media(reply)
        
        # Kirim ke 'Saved Messages' (me)
        await client.send_document(
            "me", 
            path, 
            caption=sepuh_ui("STEAL SUCCESS", f"<b>Dari:</b> {reply.from_user.first_name if reply.from_user else 'Unknown'}")
        )
        
        await message.edit("<code>Berhasil! Cek Saved Messages.</code>")
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        await message.edit(f"<b>Gagal:</b> <code>{e}</code>")

# --- FITUR TAGALL ---
@app.on_message(filters.command("tagall", ".") & filters.me)
async def tagall_sepuh(client, message):
    await message.delete()
    mems = []
    async for m in client.get_chat_members(message.chat.id):
        if not m.user.is_bot:
            mems.append(m.user.mention)
            
    for i in range(0, len(mems), 5):
        await client.send_message(message.chat.id, f"📢 <b>Tag All!</b>\n" + " ".join(mems[i:i+5]))
        await asyncio.sleep(0.3)

print("Elite Sultan Userbot Started!")
app.run()
