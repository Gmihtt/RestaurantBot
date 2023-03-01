from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Optional
from tgbot.types.types import Place


def show_places(places: List[Place], start: bool) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    line = []
    for place in places:
        line.append(InlineKeyboardButton(place['name'], callback_data="place_id" + str(place['_id'])))
        if len(line) == 2:
            markup.add(*line, row_width=2)
            line = []
    if not start:
        markup.add(InlineKeyboardButton("Назад", callback_data="back places"), row_width=2)
        markup.add(InlineKeyboardButton("Далее", callback_data="next places"), row_width=2)
    else:
        markup.add(InlineKeyboardButton("Далее", callback_data="next places"), row_width=1)
    markup.add(InlineKeyboardButton("Отправить новую точку", callback_data="new places"), row_width=1)
    return markup


def show_place() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Назад", callback_data="back places"))
    return markup

