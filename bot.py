import logging
import asyncio

from pyrogram import Client
from web import web, web_serve
from logging.handlers import RotatingFileHandler
from config import API_ID, API_HASH, BOT_TOKEN, PORT


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)


class Bot(Client):

    def __init__(self):
        super().__init__(
            "Save Rest.. bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="TechVJ"),
            workers=50,
            sleep_threshold=10
        )

      
    async def start(self):
            
        await super().start()
        LOGGER(__name__).info('Bot Started Powered By @VJ_Botz')

        #Added by @v15hnuf6n1x
        app = web.AppRunner(await web_serve())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", PORT).start()

    async def stop(self, *args):

        await super().stop()
        LOGGER(__name__).info('Bot Stopped Bye')

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s %(filename)s:%(lineno)d %(levelname).1s] %(message)s",
    datefmt="%Y-%m-%d|%H:%M:%S",
    handlers=[
        RotatingFileHandler(
            'log_file.txt',
            maxBytes=5000000,
            backupCount=3
        ),
        logging.StreamHandler()
    ]
)

if __name__ == '__main__':
    bot = Bot()
    try:
        asyncio.run(bot.run())
    except Exception as e:
        LOGGER(__name__).info(f'Error Starting: {e}')
        LOGGER(__name__).info('Starting Again')
        asyncio.run(bot.run())


