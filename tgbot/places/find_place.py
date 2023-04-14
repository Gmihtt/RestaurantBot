import logging
from typing import Optional

from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery

from tgbot.config import main_admins
from tgbot.databases.database import db, storage
import tgbot.keyboard.keyboard as keyboard
from tgbot.utils.functions import pretty_show_place, send_files


async def show_places_base(message, bot: AsyncTeleBot):
    user_id = str(message.from_user.id)
    skip = 0
    storage.add('show' + user_id, str(skip))
    loc = "{0},{1}".format(message.location.longitude, message.location.latitude)
    logging.info(str(loc))
    storage.add('place' + user_id, loc)
    places = db.find_close_place((message.location.longitude, message.location.latitude), skip=skip)
    print(places)
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
    lon, lat = float(new_loc[0]), float(new_loc[1])
    print("{0}, {1}".format(lon, lat))
    places = db.find_close_place((lon, lat), skip=skip)
    if len(places) == 0 and pred is not None:
        if pred:
            skip -= 10
            places = db.find_close_place((lon, lat), skip=skip)
        else:
            skip += 10
            places = db.find_close_place((lon, lat), skip=skip)
        await bot.send_message(chat_id=call.message.chat.id, text="""
            Вы докрутили до конца списка:(
            """, reply_markup=keyboard.show_places(places, start=skip == 0))
    else:
        await bot.send_message(chat_id=call.message.chat.id, text="""
        Вот места рядом с вами, нажмите на любое из них для подробной информации\n
        Либо пришлите новую точку
        """, reply_markup=keyboard.show_places(places, start=skip == 0))
    storage.add('show' + user_id, str(skip))


async def show_place(call: CallbackQuery, bot: AsyncTeleBot):
    if call.message is None:
        raise Exception("callback message is None")
    await bot.delete_message(call.message.chat.id, call.message.id)
    place_id = call.data[len("place_id"):]
    place = db.find_place(place_id)
    if place is None:
        raise Exception("db return None place")
    user_id = call.from_user.id
    is_admin = user_id in main_admins or db.is_admin(user_id)
    await send_files(text=pretty_show_place(place, is_admin=is_admin),
                     chat_id=call.message.chat.id,
                     files=place['files'],
                     bot=bot)
    val = storage.pop('search_by_coords' + str(user_id))
    is_admin = is_admin and (val is not None and val == "wait")
    await bot.send_message(chat_id=call.message.chat.id, text="Выберите",
                           reply_markup=keyboard.show_place(is_admin=is_admin, place_id=place_id))
