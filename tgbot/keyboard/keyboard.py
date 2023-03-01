from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Optional
from tgbot.utils.database import db
from tgbot.types.types import Place


def show_places(places: List[Place], start: bool) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for place in places:
        markup.add(InlineKeyboardButton(place.name, callback_data="place_id" + place._id))
    markup.add(InlineKeyboardButton("Далее", callback_data="next places"))
    if not start:
        markup.add(InlineKeyboardButton("Назад", callback_data="back places"))
    markup.add(InlineKeyboardButton("Отправить новую точку", callback_data="new places"))
    return markup


def show_place() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Назад", callback_data="back places"))
    return markup

