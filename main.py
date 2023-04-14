import asyncio

# telebot
from telebot.async_telebot import AsyncTeleBot

from tgbot.places.states import PlaceStates
from tgbot.states import set_state, get_state
from tgbot.handlers.handlers import welcome_handlers, admin_handlers, user_handlers, other_handlers
# config
from tgbot import config
import logging

logging.basicConfig(filename='db.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
bot = AsyncTeleBot(config.TOKEN)


def register_handlers():
    welcome_handlers(bot)
    admin_handlers(bot)
    user_handlers(bot)
    other_handlers(bot)


register_handlers()


async def run():
    await bot.polling(non_stop=True)


asyncio.run(run())
