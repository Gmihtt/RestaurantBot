from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from typing import List

from tgbot.config import main_admins
from tgbot.types.types import Place, City, PlaceType


def show_admins_chose_buttons():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Интерфейс админа', callback_data="admin_user"),
               InlineKeyboardButton('Интерфейс пользователя', callback_data="just_user"),
               row_width=1)
    return markup


def show_location_button():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button_geo = KeyboardButton(text="Отправить местоположение", request_location=True)
    markup.add(button_geo)
    return markup


def show_places(places: List[Place], start: bool) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    line = []
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


def show_place() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("🔙", callback_data="places_cur"))
    return markup


def show_admin_menu(user_id: int):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Создать рекламный пост', callback_data="add_post"),
               InlineKeyboardButton('Найти пост', callback_data="find_post"),
               row_width=1)
    markup.add(InlineKeyboardButton('Добавить место', callback_data="add_place"),
               InlineKeyboardButton('Редактировать место', callback_data="edit_place"),
               InlineKeyboardButton('Удалить место', callback_data="edit_place"),
               row_width=1)
    if user_id in main_admins:
        markup.add(InlineKeyboardButton('Добавить админа', callback_data="add_admin"),
                   InlineKeyboardButton('Удалить админа', callback_data="delete_admin"),
                   row_width=1)
    markup.add(InlineKeyboardButton('Найти место по названию', callback_data="find_place"),
               InlineKeyboardButton('Статистика', callback_data="statistics"),
               row_width=1)
    markup.add(InlineKeyboardButton('Вернуться в меню пользователя', callback_data="return_start"),
               row_width=1)
    return markup


def show_post():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Редактировать пост', callback_data="edit_post"),
               InlineKeyboardButton('Удалить пост', callback_data="delete_post"),
               InlineKeyboardButton('Вернуться в меню', callback_data="admin_user"),
               row_width=1)


def show_statistics():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Количество активных юзеров', callback_data="active_users"),
               InlineKeyboardButton('Количество юзеров за все время', callback_data="all_users"),
               InlineKeyboardButton('Количество мест', callback_data="all_places"),
               row_width=1)
    return markup


def approve_post():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Выкатить пост', callback_data="push_post"),
               InlineKeyboardButton('Редактировать', callback_data="add_post"),
               row_width=2)
    markup.add(InlineKeyboardButton('Вернуться в меню', callback_data="admin_user"),
               row_width=1)
    return markup


def chose_post_find_option(posts):
    markup = InlineKeyboardMarkup()
    line = []
    for post in posts:
        line.append(InlineKeyboardButton(post['name'], callback_data="post_id" + str(post["_id"])))
        if len(line) == 2:
            markup.add(*line, row_width=2)
            line = []
    markup.add(InlineKeyboardButton('Вернуться в меню', callback_data="admin_user"),
               row_width=1)
    return markup


def show_add_photo():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Да', callback_data="add_new_photo"),
               InlineKeyboardButton('Нет', callback_data="finish_photo"),
               row_width=1)
    return markup


def show_all_cities(cities: [City]):
    markup = InlineKeyboardMarkup()
    line = []
    for city in cities:
        line.append(InlineKeyboardButton(city['name'], callback_data="city_id" + str(city["_id"])))
        if len(line) == 2:
            markup.add(*line, row_width=2)
            line = []
    return markup


def show_all_places_type():
    places_type = [p_t.value for p_t in PlaceType]
    markup = InlineKeyboardMarkup()
    line = []
    for place_type in places_type:
        line.append(InlineKeyboardButton(place_type, callback_data="place_type" + place_type))
        if len(line) == 2:
            markup.add(*line, row_width=2)
            line = []
    return markup
