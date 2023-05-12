from typing import Optional

from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, Message

from tgbot.introduction.collection import user_collection
from tgbot.introduction.intro import show_filters
from tgbot.places import keyboards
from tgbot.places.collection import place_collection
from tgbot.places.place import Coordinates
from tgbot.places.pretty_show import pretty_show_place
from tgbot.utils.functions import send_files, count_distance
from tgbot.places.states import PlaceStates
from tgbot.utils import states, values, functions
from tgbot.config import max_distance


async def show_places_by_coordinates(message: Message, bot: AsyncTeleBot):
    user_id = str(message.from_user.id)

    message_id = values.get_value('loc_msg', user_id)
    if message_id is not None:
        await functions.delete_message(message.chat.id, int(message_id), bot)
    values.delete_value('loc_msg', user_id)

    longitude = message.location.longitude
    latitude = message.location.latitude
    loc = "{0},{1}".format(longitude, latitude)
    crds = Coordinates(
        longitude=longitude,
        latitude=latitude
    )
    places = place_collection.find_close_place(crds, user_id, skip=0, limit=0)

    count = 0
    for place in places:
        if count_distance(crds, place['coordinates']) <= max_distance:
            count += 1

    position = {
        "skip": '0',
        "location": loc,
        "count": str(count)
    }
    values.add_values_to_map('place_map', position, user_id)

    values.set_value('places', "location", str(user_id))

    if count == 0:
        text = "Под ваши фильтры не найдено заведений, либо Ваш город не поддерживается.\n" \
               "Продолжить поиск без фильтров или изменить фильтры?"
        await bot.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=keyboards.not_found()
        )
    else:
        await show_places(
            message.chat.id,
            str(message.from_user.id),
            None,
            bot
        )


async def show_next(call: CallbackQuery, bot: AsyncTeleBot):
    await show_places(
        call.message.chat.id,
        str(call.from_user.id),
        call.message.id,
        bot,
        pred=True
    )


async def show_back(call: CallbackQuery, bot: AsyncTeleBot):
    await show_places(
        call.message.chat.id,
        str(call.from_user.id),
        call.message.id,
        bot,
        pred=False
    )


async def show_cur(call: CallbackQuery, bot: AsyncTeleBot):
    await delete_place_message(call, bot)

    user_id = str(call.from_user.id)

    places_types = values.get_value('places', user_id)

    if places_types == "location":
        await show_places(
            call.message.chat.id,
            str(call.from_user.id),
            call.message.id,
            bot,
        )
    else:
        await show_favorite_places(call, bot)


async def delete_place_message(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    d = values.get_all_values_from_map('place_map', user_id)

    file_ids = values.get_list('file_ids', user_id)
    print(file_ids)
    for file_id in file_ids:
        print(file_id)
        await functions.delete_message(call.message.chat.id, int(file_id), bot)
    values.delete_list('file_ids', user_id)

    if d.get('location_id') is not None:
        await functions.delete_message(call.message.chat.id, int(d['location_id']), bot)
        values.delete_value_from_map('place_map', 'location_id', user_id)

    if d.get('phone_id') is not None:
        await functions.delete_message(call.message.chat.id, int(d['phone_id']), bot)
        values.delete_value_from_map('place_map', 'phone_id', user_id)

    if d.get('site_id') is not None:
        await functions.delete_message(call.message.chat.id, int(d['site_id']), bot)
        values.delete_value_from_map('place_map', 'site_id', user_id)


async def show_drop_filters(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    values.clean_map('filters_map', user_id)
    values.delete_list('kitchens', user_id)

    position = values.get_all_values_from_map('place_map', user_id)
    loc = position['location']
    new_loc = loc.split(",")
    crds = Coordinates(
        longitude=float(new_loc[0]),
        latitude=float(new_loc[1])
    )
    places = place_collection.find_close_place(crds, user_id, skip=0, limit=0)
    count = 0
    for place in places:
        if count_distance(crds, place['coordinates']) <= max_distance:
            count += 1

    values.add_values_to_map('place_map', {'count': str(count)}, user_id)

    await show_places(
        call.message.chat.id,
        str(user_id),
        call.message.id,
        bot,
    )


async def show_places(
        chat_id: int,
        user_id: str,
        message_id: Optional[int],
        bot: AsyncTeleBot,
        pred: Optional[bool] = None):
    await functions.delete_message(chat_id, message_id, bot)

    states.set_state(PlaceStates.ShowPlaces, user_id)
    position = values.get_all_values_from_map('place_map', user_id)
    skip = int(position['skip'])
    loc = position['location']
    count = position['count']
    new_loc = loc.split(",")
    crds = Coordinates(
        longitude=float(new_loc[0]),
        latitude=float(new_loc[1])
    )

    if pred is not None:
        skip = skip + 5 if pred else skip - 5
    start = skip == 0
    last = int(count) <= skip + 5
    places = place_collection.find_close_place(crds, user_id, skip=skip)

    if start:
        city = places[0]['city']
        user_collection.set_city(int(user_id), city)

    text = f"""Я нашел {count} заведения вокруг твоей точки!\n
Выбирай понравившееся заведение и нажимай на кнопку с его название, чтобы получить более подробную информацию о нем."""
    text_filters = await show_filters(user_id)
    text += text_filters
    await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=keyboards.show_places(crds, places, start, last)
    )
    new_show = {'skip': str(skip)}
    values.add_values_to_map('place_map', new_show, user_id)


async def show_place(call: CallbackQuery, bot: AsyncTeleBot):
    await functions.delete_message(call.message.chat.id, call.message.id, bot)
    place_id = call.data[len("place_id"):]
    place = place_collection.find_place_by_id(place_id)
    user_id = str(call.from_user.id)
    states.set_state(PlaceStates.ShowPlace, user_id)
    if len(place['files']) != 0:
        file = await send_files(text="",
                                chat_id=call.message.chat.id,
                                files=place['files'],
                                bot=bot)
        if type(file) is list:
            for f in file:
                values.add_value_to_list('file_ids', str(f.id), user_id)
        else:
            values.add_value_to_list('file_ids', str(file.id), user_id)
    user = user_collection.get_user_by_tg_id(int(user_id))

    favorite = place_id in user['favorites']

    message = await bot.send_message(
        chat_id=call.message.chat.id,
        text=pretty_show_place(place),
        reply_markup=keyboards.show_place(
            place_id=place_id,
            phone=place['phone'] is not None,
            site=place['url'] is not None,
            favorite=favorite
        )
    )

    user_collection.set_last_activity(int(user_id))

    message_info = {
        "message_id": message.id,
        "place_id": place_id
    }
    values.add_values_to_map('place_map', message_info, user_id)


async def send_location(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    d = values.get_all_values_from_map('place_map', user_id)
    place = place_collection.find_place_by_id(d['place_id'])
    location = place['coordinates']
    message = await bot.send_location(chat_id=call.message.chat.id,
                                      longitude=location['longitude'],
                                      latitude=location['latitude'])
    values.add_values_to_map('place_map', {"location_id": str(message.id)}, user_id)


async def send_phone(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    d = values.get_all_values_from_map('place_map', user_id)
    place = place_collection.find_place_by_id(d['place_id'])
    phone = place['phone'].replace(' ', '')
    message = await bot.send_message(chat_id=call.message.chat.id, text=phone)
    values.add_values_to_map('place_map', {"phone_id": str(message.id)}, user_id)


async def send_site(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    d = values.get_all_values_from_map('place_map', user_id)
    place = place_collection.find_place_by_id(d['place_id'])
    site = place['url']
    message = await bot.send_message(chat_id=call.message.chat.id, text=site)
    values.add_values_to_map('place_map', {"site_id": str(message.id)}, user_id)


async def show_favorite_places(call: CallbackQuery, bot: AsyncTeleBot):
    await functions.delete_message(call.message.chat.id, call.message.id, bot)
    user_id = str(call.from_user.id)
    states.set_state(PlaceStates.FavoritePlaces, user_id)
    pos = 0

    values.set_value('places', "favorite", str(user_id))
    user = user_collection.get_user_by_tg_id(int(user_id))
    places_ids = user['favorites']
    places = place_collection.find_places_by_ids(places_ids)

    if call.data.find("place_id") != -1:
        await show_place(call, bot)
    else:
        if call.data.find("next") != -1:
            pos = call.data[len("next"):]
        if call.data.find("prev") != -1:
            pos = call.data[len("prev"):]

    await bot.send_message(chat_id=call.message.chat.id,
                           text="Это ваши избранные места",
                           reply_markup=keyboards.show_favorite_places(places, int(pos)))


async def favorite_change(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = call.from_user.id
    states.set_state(PlaceStates.FavoriteDelete, str(user_id))

    if call.data.find("delete_yes") != -1:
        user = user_collection.get_user_by_tg_id(user_id)
        place_id = call.data[len("delete_yes"):]
        places_ids = user['favorites']
        places_ids.remove(place_id)
        user_collection.update_favorites(user_id, places_ids)
        await show_cur(call, bot)

    if call.data.find("delete_no") != -1:
        await show_cur(call, bot)

    if call.data.find("favorite_delete") != -1:
        await functions.delete_message(call.message.chat.id, call.message.id, bot)
        place_id = call.data[len("favorite_delete"):]
        await bot.send_message(chat_id=call.message.chat.id,
                               text="Ты точно хочешь удалить это место из избранного?",
                               reply_markup=keyboards.favorite_delete_approve(place_id))

    if call.data.find("favorite_add") != -1:
        user = user_collection.get_user_by_tg_id(user_id)
        place_id = call.data[len("favorite_add"):]
        places_ids = user['favorites']
        places_ids.append(place_id)
        print(places_ids)
        user_collection.update_favorites(user_id, places_ids)
        await delete_place_message(call, bot)
        call.data = "place_id" + place_id
        await show_place(call, bot)
