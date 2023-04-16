from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from tgbot.config import main_admins


def show_admin_menu(user_id: int):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Создать рекламный пост', callback_data="add_post"),
               InlineKeyboardButton('Найти пост', callback_data="find_post"),
               row_width=1)
    markup.add(InlineKeyboardButton('Добавить место', callback_data="add_place"),
               InlineKeyboardButton('Найти место', callback_data="find_place"),
               row_width=1)
    if user_id in main_admins:
        markup.add(InlineKeyboardButton('Добавить админа', callback_data="add_admin"),
                   InlineKeyboardButton('Удалить админа', callback_data="delete_admin"),
                   row_width=1)
        markup.add(InlineKeyboardButton('Статистика', callback_data="statistics"),
                   row_width=1)
    markup.add(InlineKeyboardButton('Вернуться в меню пользователя', callback_data="return_start"),
               row_width=1)
    return markup


def show_location_button():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button_geo = KeyboardButton(text="Отправить местоположение", request_location=True)
    markup.add(button_geo)
    return markup
