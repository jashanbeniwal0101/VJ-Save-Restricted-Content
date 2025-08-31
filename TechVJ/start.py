# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import time
import asyncio 
from pyrogram import Client, filters, enums
from pyrogram.errors import UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message 
from config import API_ID, API_HASH, ERROR_MESSAGE
from database.db import db
from TechVJ.strings import HELP_TXT

# For user progress tracking
user_progress = {}

# Progress callbacks
def progress_callback(done, total, user_id):  
    if user_id not in user_progress:  
        user_progress[user_id] = {'previous_done': 0, 'previous_time': time.time()}  
      
    user_data = user_progress[user_id]  
    percent = (done / total) * 100  
    completed_blocks = int(percent // 10)  
    remaining_blocks = 10 - completed_blocks  
    progress_bar = "♦" * completed_blocks + "◇" * remaining_blocks  
      
    done_mb = done / (1024 * 1024)  
    total_mb = total / (1024 * 1024)  
      
    speed = done - user_data['previous_done']  
    elapsed_time = time.time() - user_data['previous_time']  
      
    speed_bps = speed / elapsed_time if elapsed_time > 0 else 0
    speed_mbps = (speed_bps * 8) / (1024 * 1024) if speed_bps > 0 else 0
    remaining_time = (total - done) / speed_bps if speed_bps > 0 else 0  
    remaining_time_min = remaining_time / 60  
      
    final = (  
        f"╭──────────────────╮\n"  
        f"│     **__SpyLib ⚡ Uploader__**       \n"  
        f"├──────────\n"  
        f"│ {progress_bar}\n\n"  
        f"│ **__Progress:__** {percent:.2f}%\n"  
        f"│ **__Done:__** {done_mb:.2f} MB / {total_mb:.2f} MB\n"  
        f"│ **__Speed:__** {speed_mbps:.2f} Mbps\n"  
        f"│ **__ETA:__** {remaining_time_min:.2f} min\n"  
        f"╰──────────────────╯\n\n"  
        f"**__Powered by Team JB__**"  
    )  
      
    user_data['previous_done'] = done  
    user_data['previous_time'] = time.time()  
    return final  


def dl_progress_callback(done, total, user_id):  
    if user_id not in user_progress:  
        user_progress[user_id] = {'previous_done': 0, 'previous_time': time.time()}  
      
    user_data = user_progress[user_id]  
    percent = (done / total) * 100  
    completed_blocks = int(percent // 10)  
    remaining_blocks = 10 - completed_blocks  
    progress_bar = "♦" * completed_blocks + "◇" * remaining_blocks  
      
    done_mb = done / (1024 * 1024)  
    total_mb = total / (1024 * 1024)  
      
    speed = done - user_data['previous_done']  
    elapsed_time = time.time() - user_data['previous_time']  
      
    speed_bps = speed / elapsed_time if elapsed_time > 0 else 0
    speed_mbps = (speed_bps * 8) / (1024 * 1024) if speed_bps > 0 else 0
    remaining_time = (total - done) / speed_bps if speed_bps > 0 else 0  
    remaining_time_min = remaining_time / 60  
      
    final = (  
        f"╭──────────────────╮\n"  
        f"│     **__SpyLib ⚡ Downloader__**       \n"  
        f"├──────────\n"  
        f"│ {progress_bar}\n\n"  
        f"│ **__Progress:__** {percent:.2f}%\n"  
        f"│ **__Done:__** {done_mb:.2f} MB / {total_mb:.2f} MB\n"  
        f"│ **__Speed:__** {speed_mbps:.2f} Mbps\n"  
        f"│ **__ETA:__** {remaining_time_min:.2f} min\n"  
        f"╰──────────────────╯\n\n"  
        f"**__Powered by Team JB__**"  
    )  
      
    user_data['previous_done'] = done  
    user_data['previous_time'] = time.time()  
    return final  


# Batch processing temp
class batch_temp(object):
    IS_BATCH = {}


# Download status updater
async def downstatus(client, statusfile, message, chat):
    while True:
        if os.path.exists(statusfile):
            break
        await asyncio.sleep(3)
      
    while os.path.exists(statusfile):
        with open(statusfile, "r") as downread:
            txt = downread.read()
        try:
            await client.edit_message_text(chat, message.id, f"**Downloaded:** **{txt}**")
            await asyncio.sleep(10)
        except:
            await asyncio.sleep(5)


# Upload status updater
async def upstatus(client, statusfile, message, chat):
    while True:
        if os.path.exists(statusfile):
            break
        await asyncio.sleep(3)      
    while os.path.exists(statusfile):
        with open(statusfile, "r") as upread:
            txt = upread.read()
        try:
            await client.edit_message_text(chat, message.id, f"**Uploaded:** **{txt}**")
            await asyncio.sleep(10)
        except:
            await asyncio.sleep(5)


# Simple progress writer (for old code compatibility)
def progress(current, total, message, type):
    with open(f'{message.id}{type}status.txt', "w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")


# Start command
@Client.on_message(filters.command(["start"]))
async def send_start(client: Client, message: Message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
    buttons = [[
        InlineKeyboardButton("❣️ Developer", url = "https://t.me/arsh_beniwal")
    ],[
        InlineKeyboardButton('🔍 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/beniwalbots'),
        InlineKeyboardButton('🤖 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://t.me/allbotsupdates1')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(
        chat_id=message.chat.id, 
        text=f"<b>👋 Hi {message.from_user.mention}, I am Save Restricted Content Bot, I can send you restricted content by its post link.\n\nFor downloading restricted content /login first.\n\nKnow how to use bot by - /help</b>", 
        reply_markup=reply_markup, 
        reply_to_message_id=message.id
    )


# Help command
@Client.on_message(filters.command(["help"]))
async def send_help(client: Client, message: Message):
    await client.send_message(chat_id=message.chat.id, text=f"{HELP_TXT}")


# Cancel command
@Client.on_message(filters.command(["cancel"]))
async def send_cancel(client: Client, message: Message):
    batch_temp.IS_BATCH[message.from_user.id] = True
    await client.send_message(chat_id=message.chat.id, text="**Batch Successfully Cancelled.**")


# Handle messages with links
@Client.on_message(filters.text & filters.private)
async def save(client: Client, message: Message):
    if "https://t.me/" in message.text:
        if batch_temp.IS_BATCH.get(message.from_user.id, True) == False:
            return await message.reply_text("**One Task Is Already Processing. Wait For Complete It. If You Want To Cancel This Task Then Use - /cancel**")
        
        datas = message.text.split("/")
        temp = datas[-1].replace("?single","").split("-")
        fromID = int(temp[0].strip())
        try:
            toID = int(temp[1].strip())
        except:
            toID = fromID
        
        batch_temp.IS_BATCH[message.from_user.id] = False
        
        for msgid in range(fromID, toID+1):
            if batch_temp.IS_BATCH.get(message.from_user.id, True): break
            user_data = await db.get_session(message.from_user.id)
            if user_data is None:
                await message.reply("**For Downloading Restricted Content You Have To /login First.**")
                batch_temp.IS_BATCH[message.from_user.id] = True
                return
            try:
                acc = Client("saverestricted", session_string=user_data, api_hash=API_HASH, api_id=API_ID)
                await acc.connect()
            except:
                batch_temp.IS_BATCH[message.from_user.id] = True
                return await message.reply("**Your Login Session Expired. So /logout First Then Login Again By - /login**")
            
            # Private
            if "https://t.me/c/" in message.text:
                chatid = int("-100" + datas[4])
                try:
                    await handle_private(client, acc, message, chatid, msgid)
                except Exception as e:
                    if ERROR_MESSAGE:
                        await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
    
            # Bot
            elif "https://t.me/b/" in message.text:
                username = datas[4]
                try:
                    await handle_private(client, acc, message, username, msgid)
                except Exception as e:
                    if ERROR_MESSAGE:
                        await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
            
            # Public
            else:
                username = datas[3]
                try:
                    msg_obj = await client.get_messages(username, msgid)
                except UsernameNotOccupied: 
                    await client.send_message(message.chat.id, "The username is not occupied by anyone", reply_to_message_id=message.id)
                    return
                try:
                    await client.copy_message(message.chat.id, msg_obj.chat.id, msg_obj.id, reply_to_message_id=message.id)
                except:
                    try:    
                        await handle_private(client, acc, message, username, msgid)               
                    except Exception as e:
                        if ERROR_MESSAGE:
                            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)

            await asyncio.sleep(3)
        
        batch_temp.IS_BATCH[message.from_user.id] = True


# Handle private message download/upload
async def handle_private(client: Client, acc, message: Message, chatid: int, msgid: int):
    msg: Message = await acc.get_messages(chatid, msgid)
    if msg.empty: return
    msg_type = get_message_type(msg)
    if not msg_type: return
    chat = message.chat.id
    if batch_temp.IS_BATCH.get(message.from_user.id, True): return

    # Text messages
    if msg_type == "Text":
        try:
            await client.send_message(chat, msg.text, entities=msg.entities, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
            return
        except Exception as e:
            if ERROR_MESSAGE:
                await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
            return

    # Media messages
    smsg = await client.send_message(chat, '**Downloading**', reply_to_message_id=message.id)
    asyncio.create_task(downstatus(client, f'{message.id}downstatus.txt', smsg, chat))

    try:
        file_path = await acc.download_media(msg, progress=lambda d,t: dl_progress_callback(d,t,message.from_user.id))
        os.remove(f'{message.id}downstatus.txt')
    except Exception as e:
        if ERROR_MESSAGE:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
        return await smsg.delete()

    if batch_temp.IS_BATCH.get(message.from_user.id, True): return

    asyncio.create_task(upstatus(client, f'{message.id}upstatus.txt', smsg, chat))
    caption = msg.caption if msg.caption else None

    # Document
    if msg_type == "Document":
        try:
            thumb = await acc.download_media(msg.document.thumbs[0].file_id)
        except:
            thumb = None
        try:
            await client.send_document(chat, file_path, thumb=thumb, caption=caption, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML,
                                       progress=lambda d,t: progress_callback(d,t,message.from_user.id))
        except Exception as e:
            if ERROR_MESSAGE:
                await client.send_message(chat, f"Error: {e}", reply_to_message_id=message.id)
        if thumb: os.remove(thumb)

    # Video
    elif msg_type == "Video":
        try:
            thumb = await acc.download_media(msg.video.thumbs[0].file_id)
        except:
            thumb = None
        try:
            await client.send_video(chat, file_path, duration=msg.video.duration, width=msg.video.width, height=msg.video.height,
                                    thumb=thumb, caption=caption, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML,
                                    progress=lambda d,t: progress_callback(d,t,message.from_user.id))
        except Exception as e:
            if ERROR_MESSAGE:
                await client.send_message(chat, f"Error: {e}", reply_to_message_id=message.id)
        if thumb: os.remove(thumb)

    # Photo
    elif msg_type == "Photo":
        try:
            await client.send_photo(chat, file_path, caption=caption, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
        except Exception as e:
            if ERROR_MESSAGE:
                await client.send_message(chat, f"Error: {e}", reply_to_message_id=message.id)

    # Audio / Voice / Animation / Sticker
    elif msg_type == "Audio":
        try:
            thumb = await acc.download_media(msg.audio.thumbs[0].file_id)
        except:
            thumb = None
        try:
            await client.send_audio(chat, file_path, thumb=thumb, caption=caption, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML,
                                    progress=lambda d,t: progress_callback(d,t,message.from_user.id))
        except:
            pass
        if thumb: os.remove(thumb)

    elif msg_type == "Voice":
        try:
            await client.send_voice(chat, file_path, caption=caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML,
                                    progress=lambda d,t: progress_callback(d,t,message.from_user.id))
        except:
            pass

    elif msg_type == "Animation":
        try:
            await client.send_animation(chat, file_path, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
        except:
            pass

    elif msg_type == "Sticker":
        try:
            await client.send_sticker(chat, file_path, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
        except:
            pass

    if os.path.exists(f'{message.id}upstatus.txt'): 
        os.remove(f'{message.id}upstatus.txt')
    if os.path.exists(file_path):
        os.remove(file_path)
    await client.delete_messages(chat, [smsg.id])


# Determine message type
def get_message_type(msg: Message):
    try: msg.document.file_id; return "Document"
    except: pass
    try: msg.video.file_id; return "Video"
    except: pass
    try: msg.animation.file_id; return "Animation"
    except: pass
    try: msg.sticker.file_id; return "Sticker"
    except: pass
    try: msg.voice.file_id; return "Voice"
    except: pass
    try: msg.audio.file_id; return "Audio"
    except: pass
    try: msg.photo.file_id; return "Photo"
    except: pass
    try: msg.text; return "Text"
    except: pass
