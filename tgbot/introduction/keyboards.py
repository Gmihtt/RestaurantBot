from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from tgbot.config import main_admins, kitchens


def show_admin_menu(user_id: int):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Реклама', callback_data="post"))
    markup.add(InlineKeyboardButton('Места', callback_data="place"))
    if user_id in main_admins:
        markup.add(InlineKeyboardButton('Админы', callback_data="admin"))
        markup.add(InlineKeyboardButton('Статистика', callback_data="statistics"))
    markup.add(InlineKeyboardButton('Пользовательское меню', callback_data="user"))
    return markup


def filters(vegan: bool, terrace: bool, hookah: bool):
    def checker(param: bool):
        if param:
            return "да"
        else:
            return "нет"

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Рейтинг заведения', callback_data="rating"),
               InlineKeyboardButton('Веганские: ' + checker(vegan), callback_data="vegan"),
               row_width=2)
    markup.add(InlineKeyboardButton('Кухня', callback_data="chose_kitchens"),
               InlineKeyboardButton('Терраса: ' + checker(terrace), callback_data="terrace"),
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
    print(list_kitchens)
    for kitchen in list_kitchens:
        line.append(InlineKeyboardButton(kitchen, callback_data="name" + kitchen))
        if len(line) == 2:
            markup.add(*line, row_width=2)
            line = []
    if len(line) != 0:
        print(line)
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


def main_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Найти место', callback_data="find_place"),
               InlineKeyboardButton('Параметры поиска', callback_data="filters"),
               InlineKeyboardButton('Избранное', callback_data="favorites"),
               InlineKeyboardButton('Техническая поддержка', callback_data="support"),
               row_width=1)
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
