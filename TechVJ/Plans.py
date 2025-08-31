# TechVJ/plans.py
import datetime, pytz, asyncio
from pyrogram import filters
from bot import bot
from config import ADMINS
from core.mongo.plans_db import plans_db  # Make sure your Mongo functions are here

@app.on_message(filters.command("rem") & filters.user(ADMINS))
async def remove_premium(client, message):
    if len(message.command) != 2:
        return await message.reply_text("Usage: /rem user_id")

    user_id = int(message.command[1])
    data = await plans_db.check_premium(user_id)
    if data:
        await plans_db.remove_premium(user_id)
        await message.reply_text(f"✅ Premium removed for user_id {user_id}")
        await client.send_message(user_id, "Your premium has been removed.")
    else:
        await message.reply_text("User is not premium or not found.")


@app.on_message(filters.command("myplan"))
async def my_plan(client, message):
    user_id = message.from_user.id
    data = await plans_db.check_premium(user_id)
    if not data or "expire_date" not in data:
        return await message.reply_text("You do not have an active premium plan.")
    
    expiry = data["expire_date"].astimezone(pytz.timezone("Asia/Kolkata"))
    now = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
    remaining = expiry - now
    days, hours, minutes = remaining.days, remaining.seconds//3600, (remaining.seconds//60)%60

    await message.reply_text(
        f"👤 User: {message.from_user.mention}\n"
        f"⏰ Time left: {days}d {hours}h {minutes}m\n"
        f"⌛ Expiry: {expiry.strftime('%d-%m-%Y %I:%M:%S %p')}"
    )


@app.on_message(filters.command("add") & filters.user(ADMINS))
async def add_premium(client, message):
    if len(message.command) != 4:
        return await message.reply_text(
            "Usage: /add user_id 1 day/hour/min/minutes/month/year"
        )
    
    user_id = int(message.command[1])
    time_str = f"{message.command[2]} {message.command[3]}"
    
    # Convert time_str to seconds
    units = {"day":86400, "hour":3600, "min":60, "month":2592000, "year":31536000}
    try:
        number, unit = message.command[2], message.command[3].lower()
        seconds = int(number) * units.get(unit, 0)
    except:
        return await message.reply_text("Invalid time format.")

    expiry = datetime.datetime.now(pytz.timezone("Asia/Kolkata")) + datetime.timedelta(seconds=seconds)
    await plans_db.add_premium(user_id, expiry)
    await message.reply_text(f"✅ Premium added for user_id {user_id} until {expiry}")


async def premium_remover():
    while True:
        all_users = await plans_db.premium_users()
        for user_id in all_users:
            data = await plans_db.check_premium(user_id)
            if data and data["expire_date"] <= datetime.datetime.now(pytz.timezone("Asia/Kolkata")):
                await plans_db.remove_premium(user_id)
                await bot.send_message(user_id, "Your premium subscription has expired.")
        await asyncio.sleep(3600)  # check every hour
