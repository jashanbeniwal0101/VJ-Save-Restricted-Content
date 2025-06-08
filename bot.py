import logging
import asyncio
from web import web, web_serve
from pyrogram import Client
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

if __name__ == '__main__':
    bot = Bot()
    try:
        asyncio.run(bot.run())
    except Exception as e:
        LOGGER(__name__).info(f'Error Starting: {e}')
        LOGGER(__name__).info('Starting Again')
        asyncio.run(bot.run())


