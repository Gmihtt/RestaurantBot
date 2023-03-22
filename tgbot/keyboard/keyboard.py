from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from typing import List

from tgbot.config import main_admins
from tgbot.types.types import Place


def show_admins_chose_buttons():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Интерфейс пользователя', callback_data="admin_user"),
               InlineKeyboardButton('Интерфейс админа', callback_data="just_user"),
               row_width=2)
    return


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
               row_width=2)
    markup.add(InlineKeyboardButton('Добавить место', callback_data="add_place"),
               InlineKeyboardButton('Редактировать место', callback_data="edit_place"),
               row_width=2)
    if user_id in main_admins:
        markup.add(InlineKeyboardButton('Добавить админа', callback_data="add_admin"),
                   InlineKeyboardButton('Удалить админа', callback_data="delete_admin"),
                   row_width=2)
    markup.add(InlineKeyboardButton('Найти место по названию', callback_data="find_place"),
               InlineKeyboardButton('Статистика', callback_data="statistics"),
               row_width=2)
    markup.add(InlineKeyboardButton('Вернуться в меню пользователя', callback_data="return_start"),
               row_width=1)
    return markup


def show_post():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('редактировать пост', callback_data="edit_post"),
               InlineKeyboardButton('удалить пост', callback_data="delete_post"),
               row_width=2)


def show_statistics():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Количество активных юзеров', callback_data="active_users"),
               InlineKeyboardButton('Количество мест', callback_data="all_places"),
               row_width=2)
    return markup
