from typing import List

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from tgbot.config import main_admins, kitchens


def show_admin_menu(user_id: int):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Реклама', callback_data="post"))
    markup.add(InlineKeyboardButton('Места', callback_data="place"))
    if user_id in main_admins:
        markup.add(InlineKeyboardButton('Админы', callback_data="admin"))
        markup.add(InlineKeyboardButton('Статистика', callback_data="statistics"))
    markup.add(InlineKeyboardButton('Пользовательское меню', callback_data="just_user"))
    return markup


def filters(vegan: bool, business: bool, hookah: bool):
    def checker(param: bool):
        if param:
            return "ДА"
        else:
            return "НЕТ"

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Рейтинг заведения', callback_data="rating"),
               InlineKeyboardButton('Веганские: ' + checker(vegan), callback_data="vegan"),
               row_width=2)
    markup.add(InlineKeyboardButton('Кухня', callback_data="chose_kitchens"),
               InlineKeyboardButton('Бизнес-ланч: ' + checker(business), callback_data="business"),
               row_width=2)
    markup.add(InlineKeyboardButton('Средний чек', callback_data="mid_price"),
               InlineKeyboardButton('Кальян: ' + checker(hookah), callback_data="hookah"),
               row_width=2)
    markup.add(InlineKeyboardButton('Сбросить фильтры', callback_data="filters_drop"),
               InlineKeyboardButton('Перейти к поиску', callback_data="find_place"),
               InlineKeyboardButton('В меню', callback_data="main_menu"),
               row_width=1)
    return markup


def show_kitchens(pos: int):
    markup = InlineKeyboardMarkup()
    line = []
    list_kitchens = list(kitchens)[pos:pos + 10]
    for kitchen in list_kitchens:
        line.append(InlineKeyboardButton(kitchen, callback_data="name" + kitchen))
        if len(line) == 2:
            markup.add(*line, row_width=2)
            line = []
    if len(line) != 0:
        markup.add(*line, row_width=len(line))
    if 0 < pos < len(kitchens) - 10:
        markup.add(InlineKeyboardButton('⬅️', callback_data="back"),
                   InlineKeyboardButton('➡️', callback_data="next"),
                   row_width=2)
    elif pos <= 0:
        markup.add(InlineKeyboardButton('➡️', callback_data="next"), row_width=1)
    else:
        markup.add(InlineKeyboardButton('⬅️', callback_data="back"), row_width=1)
    markup.add(InlineKeyboardButton('Вернуться к параметрам', callback_data="filters", row_width=1))
    markup.add(InlineKeyboardButton('Сбросить фильтр', callback_data="drop", row_width=1))
    return markup


def main_menu(favorites: bool):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Найти место', callback_data="find_place"), row_width=1)
    markup.add(InlineKeyboardButton('Параметры поиска', callback_data="filters"), row_width=1)
    if favorites:
        markup.add(InlineKeyboardButton('Избранное', callback_data="favorites"), row_width=1)
    return markup


def mid_price():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('до 500₽', callback_data="price_500"),
               InlineKeyboardButton('до 1000₽', callback_data="price_1000"),
               InlineKeyboardButton('до 1500₽', callback_data="price_1500"),
               InlineKeyboardButton('до 2000₽', callback_data="price_2000"),
               InlineKeyboardButton('до 2500₽', callback_data="price_2500"),
               InlineKeyboardButton('до 3500₽', callback_data="price_3500"),
               InlineKeyboardButton('до 5000₽', callback_data="price_5000"),
               InlineKeyboardButton('от 5000₽', callback_data="price_5001"),
               row_width=1)
    markup.add(InlineKeyboardButton('Вернуться к параметрам', callback_data="filters", row_width=1))
    markup.add(InlineKeyboardButton('Сбросить фильтр', callback_data="drop", row_width=1))
    return markup


def rating():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('от 3.0', callback_data="rating_3.0"),
               InlineKeyboardButton('от 3.5', callback_data="rating_3.5"),
               InlineKeyboardButton('от 4.0', callback_data="rating_4.0"),
               InlineKeyboardButton('от 4.5', callback_data="rating_4.5"),
               InlineKeyboardButton('от 4.7', callback_data="rating_4.7"),
               row_width=1)
    markup.add(InlineKeyboardButton('Вернуться к параметрам', callback_data="filters", row_width=1))
    markup.add(InlineKeyboardButton('Сбросить фильтр', callback_data="drop", row_width=1))
    return markup


def find_place():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button_geo = KeyboardButton(text="📍Отправить местоположение", request_location=True)
    markup.add(button_geo)
    return markup


def back_main_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('В меню', callback_data="main_menu"), row_width=1)
    return markup


def drop_filters():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Да', callback_data="drop_yes"),
               InlineKeyboardButton('Нет', callback_data="drop_no"),
               row_width=1)
    return markup


def statistics():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Количество юзеров', callback_data="stat_all"),
               InlineKeyboardButton('Количество за час', callback_data="stat_hour"),
               InlineKeyboardButton('Количество за день', callback_data="stat_day"),
               InlineKeyboardButton('Количество за неделю', callback_data="stat_week"),
               InlineKeyboardButton('Количество за месяц', callback_data="stat_month"),
               InlineKeyboardButton('deeplink', callback_data="deeplink"),
               row_width=1)
    markup.add(InlineKeyboardButton('Вернуть в меню', callback_data="admin_user"))
    return markup


def button_admin_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Вернуться в меню', callback_data="admin_user"),
               row_width=1)
    return markup


def show_admins_chose_buttons():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Интерфейс админа', callback_data="admin_user"),
               InlineKeyboardButton('Интерфейс пользователя', callback_data="just_user"),
               row_width=1)
    return markup


def show_deeplink_stat(deeplinks: List[str], pos: int):
    markup = InlineKeyboardMarkup()
    line = []
    deeplinks = deeplinks[pos:pos + 10]
    for deeplink in deeplinks:
        line.append(InlineKeyboardButton(deeplink, callback_data="code" + deeplink))
        if len(line) == 2:
            markup.add(*line, row_width=2)
            line = []
    if len(line) != 0:
        markup.add(*line, row_width=len(line))
    if 0 < pos < len(kitchens) - 10:
        markup.add(InlineKeyboardButton('⬅️', callback_data="back"),
                   InlineKeyboardButton('➡️', callback_data="next"),
                   row_width=2)
    elif pos <= 0:
        markup.add(InlineKeyboardButton('➡️', callback_data="next"), row_width=1)
    else:
        markup.add(InlineKeyboardButton('⬅️', callback_data="back"), row_width=1)
    markup.add(InlineKeyboardButton('Вернуться к статистикам', callback_data="statistics"))
    return markup
