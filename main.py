import asyncio

# telebot
from telebot.async_telebot import AsyncTeleBot

from tgbot.handlers import handlers
# config
from tgbot import config
import logging

from tgbot.utils.functions import add_hookah_to_features

logging.basicConfig(filename='db.log',
                    filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
bot = AsyncTeleBot(config.TOKEN)

add_hookah_to_features()

print("Bot: Start")
logging.info("Bot: Start")

def register_handlers():
    handlers(bot)


register_handlers()


async def run():
    await bot.polling(non_stop=True)


asyncio.run(run())
