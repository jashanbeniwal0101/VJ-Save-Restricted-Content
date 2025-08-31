# TechVJ/speedtest.py
from pyrogram import filters
from bot import bot
from speedtest import Speedtest
from time import time

SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

def get_readable_file_size(size_in_bytes) -> str:
    index = 0
    while size_in_bytes >= 1024 and index < len(SIZE_UNITS)-1:
        size_in_bytes /= 1024
        index += 1
    return f"{round(size_in_bytes,2)}{SIZE_UNITS[index]}"

def speed_convert(size, byte=True):
    if not byte: size /= 8
    power = 1024
    index = 0
    units = ["B/s","KB/s","MB/s","GB/s","TB/s"]
    while size > power and index < len(units)-1:
        size /= power
        index +=1
    return f"{round(size,2)} {units[index]}"

@bot.on_message(filters.command("speedtest"))
async def speedtest_handler(client, message):
    msg = await message.reply_text("Running Speed Test... ⏳")
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    res = test.results.dict()
    text = (
        f"🚀 **SPEEDTEST RESULTS**\n\n"
        f"⬆ Upload: {speed_convert(res['upload'], False)}\n"
        f"⬇ Download: {speed_convert(res['download'], False)}\n"
        f"📶 Ping: {res['ping']} ms\n"
        f"📦 Data Sent: {get_readable_file_size(res['bytes_sent'])}\n"
        f"📥 Data Received: {get_readable_file_size(res['bytes_received'])}\n"
        f"🌐 Server: {res['server']['name']}, {res['server']['country']}"
    )
    try:
        await message.reply_photo(res['share'], caption=text)
    except:
        await message.reply_text(text)
    await msg.delete()
