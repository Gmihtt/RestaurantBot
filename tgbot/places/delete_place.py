from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery
from tgbot.keyboard import keyboard
from tgbot.databases.database import storage, db


async def send_search_message(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=call.message.chat.id,
                           text="Выбери как искать ресторан",
                           reply_markup=keyboard.chose_place_search())


async def search_by_coords_message(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    user_id = str(call.from_user.id)
    storage.add('search_by_coords' + user_id, "wait")
    await bot.send_message(chat_id=call.message.chat.id,
                           text="Отправьте точку ресторана через телеграм")


async def delete_place(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    place_id = call.data[len("delete_place"):]
    db.delete_place(place_id)
    await bot.send_message(chat_id=call.message.chat.id,
                           text="Место удалено",
                           reply_markup=keyboard.button_admin_menu())
