from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List

from tgbot.places.place import Place, PlaceType
from tgbot.types import City


def show_places(places: List[Place], start: bool) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    line = []
    if len(places) == 1:
        place = places[0]
        markup.add(InlineKeyboardButton(place['name'], callback_data="place_id" + str(place['_id'])))
    else:
        for place in places:
            line.append(InlineKeyboardButton(place['name'], callback_data="place_id" + str(place['_id'])))
            if len(line) == 2:
                markup.add(*line, row_width=2)
                line = []
    if not start:
        markup.add(InlineKeyboardButton('<', callback_data="places_back"),
                   InlineKeyboardButton('>', callback_data="places_next"),
                   row_width=2)
    else:
        markup.add(InlineKeyboardButton('>', callback_data="places_next"), row_width=1)
    return markup


def show_place(is_admin: bool, place_id: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    if is_admin:
        markup.add(InlineKeyboardButton("Удалить место", callback_data="delete_place" + place_id))
    markup.add(InlineKeyboardButton("🔙", callback_data="places_cur"))
    return markup


def show_all_cities(cities: [City]):
    markup = InlineKeyboardMarkup()
    line = []
    for city in cities:
        line.append(InlineKeyboardButton(city['name'], callback_data="city_id" + str(city["_id"])))
        markup.add(*line, row_width=1)
        line = []
    return markup


def show_all_places_type():
    places_type = [p_t for p_t in PlaceType]
    markup = InlineKeyboardMarkup()
    line = []
    for place_type in places_type:
        line.append(InlineKeyboardButton(place_type, callback_data="place_type" + place_type))
        markup.add(*line, row_width=1)
        line = []
    return


def approve_place():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Добавить место', callback_data="push_place"),
               InlineKeyboardButton('Начать с начала', callback_data="add_place"),
               row_width=2)
    markup.add(InlineKeyboardButton('Вернуться в меню', callback_data="admin_user"),
               row_width=1)
    return markup


def chose_place_search():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Поиск по точке', callback_data="search_by_coords"),
               row_width=1)
    markup.add(InlineKeyboardButton('Вернуться в меню', callback_data="admin_user"),
               row_width=1)
    return markup
