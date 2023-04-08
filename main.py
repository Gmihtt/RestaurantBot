import asyncio

from telebot.asyncio_filters import StateFilter

# telebot
from telebot.async_telebot import AsyncTeleBot

from tgbot.handlers.handlers import first_handlers, admin_handlers, user_handlers, other_handlers
# config
from tgbot import config
import logging

logging.basicConfig(filename='db.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
bot = AsyncTeleBot(config.TOKEN)


def register_handlers():
    first_handlers(bot)
    admin_handlers(bot)
    user_handlers(bot)
    other_handlers(bot)


register_handlers()


async def run():
    await bot.polling(non_stop=True)


bot.add_custom_filter(StateFilter(bot))

asyncio.run(run())
