from datetime import datetime
from typing import Optional

from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery
import tgbot.keyboard.keyboard as keyboard


async def show_admin_menu(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(call.message.chat.id, call.message.id)
    await bot.send_message(chat_id=call.message.chat.id, text="""
    Основное меню:
    """, reply_markup=keyboard.show_admin_menu(call.from_user.id))


async def show_statistics(call: CallbackQuery, bot: AsyncTeleBot):
    pass


async def add_advertising_post():
    pass
