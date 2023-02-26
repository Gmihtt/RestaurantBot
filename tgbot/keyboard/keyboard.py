from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Optional
from tgbot.utils.database import db
from tgbot.types.types import Group, Place


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


def show_group(user_id: str, group_name: str) -> Optional[InlineKeyboardMarkup]:
    places: List[Place] = db.get_group_place(user_id, group_name)
    if places:
        markup = InlineKeyboardMarkup()
        markup.row_width = len(places)
        for place in places:
            markup.add(InlineKeyboardButton(place.name, callback_data=place.name))
        markup.add(InlineKeyboardButton("Добавить место", callback_data="add place"))
        markup.add(InlineKeyboardButton("Назад", callback_data="back"))
        return markup
    return None
