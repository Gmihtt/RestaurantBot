from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Optional
from tgbot.utils.database import db
from tgbot.types.types import Place


def start_markup(user_id: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    groups: List[Group] = db.get_groups(user_id)
    if groups:
        markup.row_width = len(groups)
        for group in groups:
            markup.add(InlineKeyboardButton(group.name, callback_data=group.name))
    markup.add(InlineKeyboardButton("Поиск", callback_data="search"))
    markup.add(InlineKeyboardButton("Добавить группу", callback_data="add group"))
    return markup
