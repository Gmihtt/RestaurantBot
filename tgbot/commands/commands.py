from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove

from tgbot.types.types import pretty_show_place
from tgbot.utils.database import db, storage
import tgbot.keyboard.keyboard as keyboard
from tgbot.utils.functions import generate_places


async def send_welcome(message: Message, bot: AsyncTeleBot):
    storage.add(str(message.from_user.id), "0,10")
    await bot.reply_to(message, """
    Привет!\nПришли мне свою геопозицию и я покажу какие места есть рядом с тобой
    """)


async def show_places(message, bot: AsyncTeleBot):
    val = storage.get(str(message.from_user.id))
    if val is None:
        raise Exception("storage return None")
    new_val = val.split(",")
    if len(new_val) != 2:
        raise Exception("storage return: " + val)
    skip, limit = int(new_val[0]), int(new_val[1])
    print("{0}, {1}".format(message.location.longitude, message.location.latitude))
    places = db.find_close_place((message.location.longitude, message.location.latitude), skip=skip, limit=limit)
    if len(places) == 0:
        raise Exception("db return empty places list")
    start = skip == 0 and limit == 10
    await bot.reply_to(message, """
    Вот места рядом с вами, нажмите на любое из них для подробной информации
    """, reply_markup=keyboard.show_places(places, start))
    storage.add(str(message.from_user.id), str(skip) + "," + str(limit + 10))


async def show_place(call: CallbackQuery, bot: AsyncTeleBot):
    place_id = call.data[len("place_id"):]
    place = db.find_place(place_id)
    if place is None:
        raise Exception("db return None place")
    await bot.send_message(chat_id=call.message.chat.id, text=pretty_show_place(place), reply_markup=keyboard.show_place())


async def send_help(message: Message, bot: AsyncTeleBot):
    generate_places(100)
    await bot.set_state(message.from_user.id, message.chat.id)
    await bot.reply_to(message, "help")
