import asyncio

import typing

from telebot.asyncio_filters import StateFilter
from telebot.asyncio_storage import StateMemoryStorage

from tgbot.commands.commands import send_welcome, send_help

# handlers
from tgbot.handlers.admin import admin_user

# states
from tgbot.states.user_state import UserState

# utils
from tgbot.utils.database import Database

# telebot
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
# config
from tgbot import config

db = Database()

bot = AsyncTeleBot(config.TOKEN, state_storage=StateMemoryStorage())


def register_handlers():
    bot.register_message_handler(admin_user, commands=['start'], admin=True, pass_bot=True)
    bot.register_message_handler(send_welcome, commands=['start', 'restart'], pass_bot=True)
    bot.register_message_handler(send_help, commands=['help'], pass_bot=True)


register_handlers()


@bot.message_handler(state=UserState.START)
async def echo_message(message: Message):
    await bot.reply_to(message, message.text)


async def run():
    await bot.polling(non_stop=True)


bot.add_custom_filter(StateFilter(bot))

asyncio.run(run())
