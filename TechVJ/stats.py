# TechVJ/stats.py
import time, sys
from pyrogram import filters
from bot import bot
from config import ADMINS
from core.mongo.users_db import get_users
from core.mongo.plans_db import premium_users

start_time = time.time()

def format_time():
    seconds = int(time.time() - start_time)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    return f"{d}d {h}h {m}m {s}s"

@bot.on_message(filters.command("stats") & filters.user(ADMINS))
async def stats_handler(client, message):
    start = time.time()
    users = len(await get_users())
    premium = await premium_users()
    ping = round((time.time()-start)*1000)
    
    await message.reply_text(
        f"**Bot Stats:**\n\n"
        f"🏓 Ping: {ping}ms\n"
        f"📊 Total Users: {users}\n"
        f"📈 Premium Users: {len(premium)}\n"
        f"⚙️ Uptime: {format_time()}\n"
        f"🐍 Python: {sys.version.split()[0]}"
    )
