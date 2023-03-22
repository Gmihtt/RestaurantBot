from typing import Optional

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery

from tgbot.config import support, main_admins
from tgbot.types.types import pretty_show_place
from tgbot.utils.database import db, storage
import tgbot.keyboard.keyboard as keyboard


async def show_admin_menu(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(call.message.chat.id, call.message.id)
    await bot.send_message(chat_id=call.message.chat.id, text="""
    Основное меню:
    """, reply_markup=keyboard.show_admin_menu(call.message.from_user.id))


async def send_add_post_name_message(call: CallbackQuery, bot: AsyncTeleBot):
    if call.message is None:
        raise Exception("callback message is None")
    await bot.delete_message(call.message.chat.id, call.message.id)
    user_id = str(call.from_user.id)
    storage.add('admin_post_name' + user_id, "blah")
    await bot.send_message(chat_id=call.message.chat.id, text="""Пришли мне название поста""")


async def send_add_post_body_message(message: Message, bot: AsyncTeleBot):
    user_id = str(message.from_user.id)
    name = message.text
    storage.add('admin_post_body' + user_id, name)
    await bot.send_message(chat_id=message.chat.id, text="""Напиши текст поста""")


async def send_add_post_body_message(message: Message, bot: AsyncTeleBot):
    user_id = str(message.from_user.id)
    name = storage.get('admin_post_body' + user_id)
    body = message.text
    db.add
    await bot.send_message(chat_id=message.chat.id, text="""Напиши текст поста""")


async def show_statistics(call: CallbackQuery, bot: AsyncTeleBot):
    pass


async def add_advertising_post():
    pass