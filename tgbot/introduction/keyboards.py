from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from tgbot.config import main_admins


def show_admin_menu(user_id: int):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Реклама', callback_data="post"))
    markup.add(InlineKeyboardButton('Места', callback_data="place"))
    if user_id in main_admins:
        markup.add(InlineKeyboardButton('Админы', callback_data="admin"))
        markup.add(InlineKeyboardButton('Статистика', callback_data="statistics"))
    markup.add(InlineKeyboardButton('Пользовательское меню', callback_data="user"))
    return markup


def show_location_button():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button_geo = KeyboardButton(text="Отправить местоположение", request_location=True)
    markup.add(button_geo)
    return markup
