from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List

from tgbot.config import cities, places_types, kitchens
from tgbot.places.place import Place, PlaceType


def show_places(places: List[Place], start: bool) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    line = []
    for place in places:
        line.append(InlineKeyboardButton(place['name'], callback_data="place_id" + str(place['_id'])))
        if len(line) == 2:
            markup.add(*line, row_width=2)
            line = []

    if len(line) == 1:
        markup.add(*line, row_width=1)

    if not start:
        markup.add(InlineKeyboardButton('<', callback_data="places_back"),
                   InlineKeyboardButton('>', callback_data="places_next"),
                   row_width=2)
    else:
        markup.add(InlineKeyboardButton('>', callback_data="places_next"), row_width=1)
    return markup


def show_place() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Вернуться к списку", callback_data="places_cur"))
    markup.add(InlineKeyboardButton("Точка ресторана", callback_data="place_position"))
    return markup


def show_all_cities():
    markup = InlineKeyboardMarkup()
    line = []
    for city in cities:
        line.append(InlineKeyboardButton(city, callback_data=city))
        markup.add(*line, row_width=1)
        line = []
    return markup


def show_all_places_types():
    markup = InlineKeyboardMarkup()
    line = []
    for place_type in places_types:
        line.append(InlineKeyboardButton(place_type, callback_data=place_type))
        markup.add(*line, row_width=1)
        line = []
    return markup


def show_all_kitchens():
    markup = InlineKeyboardMarkup()
    line = []
    print(len(kitchens))
    for kitchen in kitchens:
        line.append(InlineKeyboardButton(kitchen, callback_data=kitchen))
        if len(line) == 3:
            markup.add(*line, row_width=3)
            line = []
    if len(line) != 0:
        markup.add(*line, row_width=len(line))
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
               InlineKeyboardButton('Начать с начала', callback_data="place"),
               row_width=2)
    markup.add(InlineKeyboardButton('Вернуться в меню', callback_data="admin_user"),
               row_width=1)
    return markup
