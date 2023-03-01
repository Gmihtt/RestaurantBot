import asyncio

import typing

from telebot.asyncio_filters import StateFilter
from telebot.asyncio_storage import StateMemoryStorage

from tgbot.commands.commands import send_welcome, send_help, show_places, show_place

# states
from tgbot.states.user_state import States

# telebot
from telebot.async_telebot import AsyncTeleBot
# config
from tgbot import config
from tgbot.utils.functions import filter_place_prefix

bot = AsyncTeleBot(config.TOKEN, state_storage=StateMemoryStorage())


def register_handlers():
    bot.register_message_handler(send_welcome, commands=['start', 'restart'], pass_bot=True)
    bot.register_message_handler(send_help, commands=['help'], pass_bot=True)
    bot.register_message_handler(show_places, content_types=['location'], pass_bot=True)
    bot.register_callback_query_handler(show_place, func=filter_place_prefix, pass_bot=True)


register_handlers()


async def run():
    await bot.polling(non_stop=True)


bot.add_custom_filter(StateFilter(bot))

asyncio.run(run())
