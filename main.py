import os
from pyrogram import Client

# Kode ini akan mengambil data dari pengaturan "Variables" di Railway, bukan dari file teks
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION")

app = Client("Elite_Sultan", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
# --- THEME ENGINE V3 (ULTRA PREMIUM) ---
# Desain ini sudah pakai font mewah dan layout simetris
def sultan_ui(title, body):
    return (
        f"<b>╔════ {title} ════╗</b>\n"
        f"<b>  💎 𝖲𝖳𝖠𝖳𝖴𝖲:</b> <code>𝖤𝖫𝖨𝖳𝖤 𝖴𝖲𝖤𝖱</code>\n"
        f"<b>  🛡 𝖲𝖤𝖢𝖴𝖱𝖨𝖳𝖸:</b> <code>𝖠𝖢𝖳𝖨𝖵𝖤</code>\n"
        f"<b>╚════════════════════╝</b>\n"
        f"<b>{body}</b>\n"
        f"<b>──────────────</b>"
    )

# --- 1. FITUR TAG ALL (SILENT & FAST) ---
@app.on_message(filters.command("tagall", ".") & filters.me)
async def tagall_sultan(client, message):
    await message.delete()
    chat_id = message.chat.id
    members = []
    async for m in client.get_chat_members(chat_id):
        if not m.user.is_bot: members.append(m.user.mention)
    
    for i in range(0, len(members), 5):
        await client.send_message(chat_id, f"⚡️ 𝖯𝖱𝖤𝖬𝖨𝖴𝖬 𝖠𝖭𝖭𝖮𝖴𝖭𝖢𝖤 ⚡️\n" + " ".join(members[i:i+5]))
        await asyncio.sleep(1)

# --- 2. FITUR AUTO PROMO (MARKETING AUTOMATION) ---
@app.on_message(filters.command("setpromo", ".") & filters.me)
async def set_promo(_, message):
    # Cara pakai: .setpromo [ID Grup] | [Pesan]
    data = message.text.split(None, 1)[1].split("|")
    gid = int(data[0].strip())
    text = data[1].strip()
    await message.edit("<code>✅ Promo Engine Started...</code>")
    while True:
        await app.send_message(gid, sultan_ui("𝖠𝖴𝖳𝖮 𝖯𝖱𝖮𝖬𝖮", f"📢 {text}"))
        await asyncio.sleep(3600) # Sebar tiap 1 jam

# --- 3. FITUR STEAL MEDIA (VIEW ONCE BYPASS) ---
@app.on_message(filters.command("steal", ".") & filters.me)
async def steal_cmd(client, message):
    if not message.reply_to_message: return
    await message.edit("<code>📥 Extracting Media...</code>")
    await client.copy_message("me", message.chat.id, message.reply_to_message.id)
    await message.edit("<code>✅ Media Secured in Saved Messages.</code>")

# --- 4. FITUR FAKE PREMIUM LOOK (AUTO) ---
@app.on_message(filters.me & ~filters.command(["status", "tagall", "steal"], "."))
async def premium_effect(_, message):
    # Menambahkan emoji petir otomatis di setiap chatmu
    if message.text:
        try: await message.edit(f"{message.text}  ⚡️")
        except: pass

# --- 5. FITUR GHOST READ (BACA DIAM-DIAM) ---
@app.on_message(filters.command("read", ".") & filters.me)
async def ghost_read(client, message):
    if message.reply_to_message:
        msg = message.reply_to_message
        res = f"👤 𝖥𝗋𝗈𝗆: {msg.from_user.first_name}\n💬 𝖬𝗌𝖌: {msg.text}"
        await message.edit(sultan_ui("𝖦𝖧𝖮𝖲𝖳 𝖱𝖤𝖠𝖣𝖤𝖱", res))

# --- 6. STATUS DASHBOARD (MAHAL) ---
@app.on_message(filters.command("status", ".") & filters.me)
async def status_dash(_, message):
    start = datetime.now()
    await message.edit("<code>Connecting to Elite Server...</code>")
    ping = (datetime.now() - start).microseconds / 1000
    res = f"📡 𝖫𝖺𝗍𝖾𝗇𝖼𝗒: <code>{ping}ms</code>\n💎 𝖯𝗅𝖺𝗇: <code>𝖲𝗎𝗅𝗍𝖺𝗇-𝖷</code>\n🛰 𝖲𝖾𝗋𝗏𝖾𝗋: <code>𝖱𝖺𝗂𝗅𝗐𝖺𝗒.𝖺𝗉𝗉</code>"
    await message.edit(sultan_ui("𝖲𝖸𝖲𝖳𝖤𝖬 𝖢𝖧𝖤𝖢𝖪", res))

app.run()