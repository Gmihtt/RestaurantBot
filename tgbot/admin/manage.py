from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, Message

from tgbot.common_keyboards import button_admin_menu
from tgbot.databases.database import db
from tgbot.databases.redis_storage import storage


async def add_admin_message(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    storage.add('add_admin' + user_id, "wait")
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=call.message.chat.id,
                           text="""Пришлите username того, кого вы хотите добавить в админы\n"""
                                "Этот человек уже должен был воспользовать ботом, а его username должен быть виден\n"
                                "Если username это @user_name то вы должны прислать просто user_name")


async def add_user_to_admin(message: Message, bot: AsyncTeleBot):
    username = message.text
    res = db.add_admin(username)
    user_id = str(message.from_user.id)
    storage.delete('add_admin' + user_id)
    if res is None:
        await bot.send_message(chat_id=message.chat.id,
                               text="""Не вышло добавить юзера в админы""",
                               reply_markup=button_admin_menu())
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text="""Пользователь добавлен""",
                               reply_markup=button_admin_menu())
