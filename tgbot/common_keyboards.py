from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def show_file(suffix: str):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Да', callback_data="add_new_file_" + suffix),
               InlineKeyboardButton('Нет', callback_data="finish_file_" + suffix),
               row_width=1)
    return markup

