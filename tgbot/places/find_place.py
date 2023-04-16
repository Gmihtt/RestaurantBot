from typing import Optional

from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery

from tgbot.databases.database import db
import tgbot.keyboard.keyboard as keyboard
from tgbot.places.pretty_show import pretty_show_place
from tgbot.utils.functions import send_files, is_admin
from tgbot.places.states import PlaceStates
from tgbot.utils import states, values


async def show_places_by_coordinates(message, bot: AsyncTeleBot):
    user_id = str(message.from_user.id)
    states.set_state(PlaceStates.ShowPlaces, user_id)
    skip = 0
    loc = "{0},{1}".format(message.location.longitude, message.location.latitude)
    position = {
        "show": str(skip),
        "location": loc
    }
    values.add_values_to_map(position, user_id)
    places = db.find_close_place((message.location.longitude, message.location.latitude), skip=skip)
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
    await bot.delete_message(call.message.chat.id, call.message.id)
    user_id = str(call.from_user.id)
    position = values.get_all_values_from_map(user_id)
    val = position['show']
    loc = position['location']
    skip = int(val)
    new_loc = loc.split(",")
    if pred is not None:
        skip = skip + 10 if pred else skip - 10
    lon, lat = float(new_loc[0]), float(new_loc[1])
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
    new_show = {'show': str(skip)}
    values.add_values_to_map(new_show, user_id)


async def show_place(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(call.message.chat.id, call.message.id)
    place_id = call.data[len("place_id"):]
    place = db.find_place(place_id)
    user_id = str(call.from_user.id)
    states.set_state(PlaceStates.ShowPlace, user_id)
    await send_files(text=pretty_show_place(place, is_admin=is_admin(user_id)),
                     chat_id=call.message.chat.id,
                     files=place['files'],
                     bot=bot)
    await bot.send_message(chat_id=call.message.chat.id, text="Выберите",
                           reply_markup=keyboard.show_place(is_admin=is_admin(user_id), place_id=place_id))
