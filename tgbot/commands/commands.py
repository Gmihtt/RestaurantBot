from typing import Optional

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery

from tgbot.config import support, main_admins
from tgbot.types.types import pretty_show_place, User
from tgbot.utils.database import db, storage
import tgbot.keyboard.keyboard as keyboard


async def check_welcome(message: Message, bot: AsyncTeleBot):
    user_id = message.from_user.id
    user = User(
        _id=None,
        user_tg_id=user_id,
        username=message.from_user.username
    )
    db.add_user(user)
    if message.from_user.id in main_admins or db.is_admin(user_id):
        await bot.reply_to(message, """
        \nВыберете интерфейс
        """, reply_markup=keyboard.show_admins_chose_buttons())
    else:
        await send_welcome(message, bot)


async def send_welcome(message: Message, bot: AsyncTeleBot):
    await bot.reply_to(message, """
    \nПришли мне свое местоположение и я покажу какие места есть рядом с тобой
    """, reply_markup=keyboard.show_location_button())


async def show_places_base(message, bot: AsyncTeleBot):
    user_id = str(message.from_user.id)
    skip = 0
    storage.add('show' + user_id, str(skip))
    loc = "{0},{1}".format(message.location.longitude, message.location.latitude)
    storage.add('place' + user_id, loc)
    places = db.find_close_place((message.location.longitude, message.location.latitude), skip=skip)
    if len(places) == 0:
        raise Exception("db return empty places list")
    await bot.reply_to(message, """
    Вот места рядом с вами, нажмите на любое из них для подробной информации\n
    Либо пришлите новую точку
    """, reply_markup=keyboard.show_places(places, start=True))


async def show_next(call: CallbackQuery, bot: AsyncTeleBot):
    await show_places_next_or_back(call, bot, pred=True)


async def show_back(call: CallbackQuery, bot: AsyncTeleBot):
    await show_places_next_or_back(call, bot, pred=False)


async def show_cur(call: CallbackQuery, bot: AsyncTeleBot):
    await show_places_next_or_back(call, bot)


async def show_places_next_or_back(call: CallbackQuery, bot: AsyncTeleBot, pred: Optional[bool] = None):
    if call.message is None:
        raise Exception("callback message is None")
    await bot.delete_message(call.message.chat.id, call.message.id)
    user_id = str(call.from_user.id)
    val = storage.get('show' + user_id)
    loc = storage.get('place' + user_id)
    if val is None or loc is None:
        raise Exception("storage return None")
    skip = int(val)
    print(val)
    new_loc = loc.split(",")
    if len(new_loc) != 2:
        raise Exception("storage return: " + loc)
    if pred is not None:
        skip = skip + 10 if pred else skip - 10
    storage.add('show' + user_id, str(skip))
    lon, lat = float(new_loc[0]), float(new_loc[1])
    print("{0}, {1}".format(lon, lat))
    places = db.find_close_place((lon, lat), skip=skip)
    if len(places) == 0:
        raise Exception("db return empty places list")
    start = skip == 0
    await bot.send_message(chat_id=call.message.chat.id, text="""
    Вот места рядом с вами, нажмите на любое из них для подробной информации\n
    Либо пришлите новую точку
    """, reply_markup=keyboard.show_places(places, start=start))


async def show_place(call: CallbackQuery, bot: AsyncTeleBot):
    if call.message is None:
        raise Exception("callback message is None")
    await bot.delete_message(call.message.chat.id, call.message.id)
    place_id = call.data[len("place_id"):]
    place = db.find_place(place_id)
    if place is None:
        raise Exception("db return None place")
    await bot.send_message(chat_id=call.message.chat.id, text=pretty_show_place(place),
                           reply_markup=keyboard.show_place())


async def send_help(message: Message, bot: AsyncTeleBot):
    await bot.reply_to(message, """
    Кажется Вы ввели какое-то странное сообщение, либо Вам нужна помощь.\n
    Если Вам нужна помощь, то напишите: """ + support)
