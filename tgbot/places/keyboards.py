from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List

from tgbot.config import max_distance
from tgbot.places.place import Place, Coordinates
from tgbot.utils import functions
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
        rating = ""
        if place.get('place').get('rating') is not None:
            r = place['place']['rating']
            rating = str(round(r, 1)) + " ⭐️ "
        if distance <= max_distance:
            if distance >= 1:
                distance = str(round(distance, 1))

                markup.add(InlineKeyboardButton(
                    rating + place['name'] + ' (' + distance + 'км' + ')',
                    callback_data="place_id" + str(place['_id'])
                ),
                    row_width=1
                )
            else:
                distance = int(round(distance, 4) * 1000)

                markup.add(InlineKeyboardButton(
                    rating + place['name'] + ' (' + functions.create_metre_str(distance) + ')',
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
    elif max_radius and not start:
        markup.add(InlineKeyboardButton('⬅️', callback_data="places_back"), row_width=1)
    markup.add(InlineKeyboardButton('Сбросить фильтры', callback_data="filters_drop"))
    markup.add(InlineKeyboardButton('В главное меню', callback_data="main_menu"))
    return markup


def show_place(place_id: str,
               phone: bool,
               site: bool,
               favorite: bool) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📍Показать на карте", callback_data="place_position"))
    if phone:
        markup.add(InlineKeyboardButton("📞 Позвонить", callback_data="place_phone"))
    if site:
        markup.add(InlineKeyboardButton("🌐 Сайт", callback_data="place_site"))
    if favorite:
        markup.add(InlineKeyboardButton("💔 Удалить из избранного", callback_data="favorite_delete" + place_id))
    if not favorite:
        markup.add(InlineKeyboardButton("❤️ Добавить в избранное", callback_data="favorite_add" + place_id))
    markup.add(InlineKeyboardButton("⬅️ Назад", callback_data="places_cur"))
    return markup


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


def show_favorite_places(places: List[Place], pos: int):
    markup = InlineKeyboardMarkup()
    cur_places = places[pos: pos + 5]
    for cur_place in cur_places:
        markup.add(InlineKeyboardButton(cur_place['name'],
                                        callback_data="place_id" + str(cur_place['_id']),
                                        row_width=1))

    if 0 < pos < len(places) - 5:
        markup.add(InlineKeyboardButton('⬅️', callback_data="back" + str(pos - 5)),
                   InlineKeyboardButton('➡️', callback_data="next" + str(pos + 5)),
                   row_width=2)
    elif pos == 0 and len(places) >= 5:
        markup.add(InlineKeyboardButton('➡️', callback_data="next" + str(pos + 5)),
                   row_width=1)
    elif pos >= 5:
        markup.add(InlineKeyboardButton('⬅️', callback_data="back" + str(pos - 5)),
                   row_width=1)
    markup.add(InlineKeyboardButton('В меню', callback_data="main_menu"))
    return markup


def favorite_delete_approve(place_id: str):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Да", callback_data="delete_yes" + place_id),
               InlineKeyboardButton("Нет", callback_data="delete_no" + place_id),
               row_width=2)
    return markup
