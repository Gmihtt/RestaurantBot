from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def show_admins_chose_buttons():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Интерфейс админа', callback_data="admin_user"),
               InlineKeyboardButton('Интерфейс пользователя', callback_data="just_user"),
               row_width=1)
    return markup


def show_file(suffix: str):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Да', callback_data="add_new_file_" + suffix),
               InlineKeyboardButton('Нет', callback_data="finish_file_" + suffix),
               row_width=1)
    return markup


def button_admin_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Вернуться в меню', callback_data="admin_user"),
               row_width=1)
    return markup
