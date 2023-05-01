from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List

from tgbot.config import max_distance
from tgbot.places.place import Place, PlaceType, Coordinates
from tgbot.utils.functions import count_distance


def show_places(
        crds1: Coordinates,
        places: List[Place],
        start: bool,
        last: bool
) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    max_radius = False
    for place in places:
        crds2 = place['coordinates']
        distance = count_distance(crds1, crds2)
        if distance <= max_distance:
            distance = str(round(distance, 1))

            markup.add(InlineKeyboardButton(
                place['name'] + ' (' + distance + 'км' + ')',
                callback_data="place_id" + str(place['_id'])
            ),
                row_width=1
            )
        else:
            max_radius = True
            break

    if not start and not max_radius and not last:
        markup.add(InlineKeyboardButton('⬅️', callback_data="places_back"),
                   InlineKeyboardButton('➡️', callback_data="places_next"),
                   row_width=2)
    elif start and not last:
        markup.add(InlineKeyboardButton('➡️', callback_data="places_next"), row_width=1)
    elif max_radius or not start:
        markup.add(InlineKeyboardButton('⬅️', callback_data="places_back"), row_width=1)
    markup.add(InlineKeyboardButton('Сбросить фильтры', callback_data="filters_drop"))
    markup.add(InlineKeyboardButton('В меню', callback_data="main_menu"))
    return markup


def show_place(phone: bool, site: bool) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Показать на карте", callback_data="place_position"))
    if phone:
        markup.add(InlineKeyboardButton("Позвонить", callback_data="place_phone"))
    if site:
        markup.add(InlineKeyboardButton("Сайт", callback_data="place_site"))
    markup.add(InlineKeyboardButton("Вернуться к списку", callback_data="places_cur"))
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


def not_found():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Без фильтров', callback_data="without_filters"),
               InlineKeyboardButton('К фильтрам', callback_data="filters"),
               row_width=2)
    return markup
