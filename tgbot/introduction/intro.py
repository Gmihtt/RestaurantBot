import logging
from datetime import datetime
from typing import Optional

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery

from tgbot.introduction import user
from tgbot.introduction.collection import user_collection, stat_collection
from tgbot.introduction.user import User
from tgbot.photos import save_photos
from tgbot.places.place import PlaceType
from tgbot.places.pretty_show import pretty_show_place_type
from tgbot.texts import intro_text, place_point_text
from tgbot.utils import states, values, functions
from tgbot.config import main_admins
from tgbot.introduction import keyboards
from tgbot.introduction.states import IntroStates


def extract_unique_code(text: str) -> Optional[str]:
    return text.split()[1] if len(text.split()) > 1 else None


async def check_welcome(message: Message, bot: AsyncTeleBot):
    user_id = message.from_user.id
    states.set_state(IntroStates.Welcome, str(user_id))
    if user_id in main_admins: #or user_collection.is_admin(user_id):
        await bot.reply_to(message, """
Выбери интерфейс
""", reply_markup=keyboards.show_admins_chose_buttons())
    else:
        code = extract_unique_code(message.text)
        await send_welcome(message, bot, code)


async def send_welcome(message: Message, bot: AsyncTeleBot, code: Optional[str] = None):
    await welcome(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        username=message.from_user.username,
        bot=bot,
        code=code,)


async def send_welcome_callback(call: CallbackQuery, bot: AsyncTeleBot):
    await functions.delete_message(call.message.chat.id, call.message.id, bot)
    await welcome(
        user_id=call.from_user.id,
        chat_id=call.message.chat.id,
        username=call.from_user.username,
        bot=bot)


async def welcome(
        user_id: int,
        chat_id: int,
        username: Optional[str],
        bot: AsyncTeleBot,
        code: Optional[str] = None,):
    user_id = user_id
    states.set_state(IntroStates.MainMenu, str(user_id))
    u = await save_user(
        user_id=user_id,
        chat_id=chat_id,
        username=username,
        code=code
    )
    await functions.delete_old_msg(chat_id, bot)
    await bot.send_message(
        chat_id=chat_id,
        text=intro_text,
        reply_markup=keyboards.main_menu(favorites=u['favorites'] != []),
        parse_mode="html"
    )
    logging.info(f"user start: {user_id}")


async def save_user(user_id: int, chat_id: int, username: Optional[str], code: Optional[str] = None) -> User:
    u = user_collection.get_user_by_tg_id(user_id)
    if u is None:
        u = user.User(
            _id=None,
            user_tg_id=user_id,
            chat_id=chat_id,
            username=username,
            city="",
            is_admin=False,
            favorites=[],
            last_activity=datetime.now()
        )
        _id = user_collection.add_user(u)
        if code is not None:
            stat_collection.new_user_deeplink(code, _id)
    return u


async def show_admin_menu(call: CallbackQuery, bot: AsyncTeleBot):
    await save_photos(bot)
    await functions.delete_message(call.message.chat.id, call.message.id, bot)
    user_id = call.from_user.id
    states.set_state(IntroStates.AdminMenu, str(user_id))
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="""Основное меню:""",
        reply_markup=keyboards.show_admin_menu(call.from_user.id)
    )


async def place_preview(call: CallbackQuery, bot: AsyncTeleBot):
    await functions.delete_message(call.message.chat.id, call.message.id, bot)
    user_id = str(call.from_user.id)
    text = place_point_text
    text_filter = await show_filters(user_id)
    text += text_filter
    message = await bot.send_message(
        chat_id=call.message.chat.id,
        text="Отправь местоположение",
        reply_markup=keyboards.find_place()
    )
    chat_id = call.message.chat.id
    values.set_value('msg_id_delete', str(message.id), str(chat_id))
    values.set_value('loc_msg', str(message.id), user_id)
    await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=keyboards.back_main_menu(),
        parse_mode="html"
    )


async def show_filters(user_id: str):
    text = ""
    filters_map = values.get_all_values_from_map('filters_map', user_id)
    if filters_map:
        text += "\n" + "Выбранные фильтры: "
        kitchens = values.get_list('kitchens', user_id)
        if kitchens is not None and kitchens != []:
            text += '\n\n' + "Кухни: <i>"
            for kitchen in kitchens:
                text += kitchen + " "
            text += "</i>"

        if filters_map.get('mid_price') is not None:
            mid_price = int(filters_map['mid_price'])
            text += '\n' + "Средний чек от: <i>" + str(mid_price) + '₽</i>'

        if filters_map.get('rating') is not None:
            rating = filters_map['rating']
            text += '\n' + "Рейтинг от: <i>" + rating + "</i>"

        if values.get_list('place_types', user_id):
            place_types = values.get_list('place_types', user_id)
            text += '\n' + "Тип заведений: <i>"
            for p_t in place_types:
                text += pretty_show_place_type(PlaceType(p_t)) + " "
            text += "</i>"

        if filters_map.get('business') is not None and filters_map['business'] == 'True':
            text += '\n' + "Бизнес-ланч: <i>" + ("да" if filters_map['business'] == 'True' else "нет") + "</i>"

        if filters_map.get('vegan') is not None and filters_map['vegan'] == 'True':
            text += '\n' + "Веганское меню: <i>" + ("да" if filters_map['vegan'] == 'True' else "нет") + "</i>"

        if filters_map.get('terrace') is not None and filters_map['terrace'] == 'True':
            text += '\n' + "Летняя терраса: <i>" + ("да" if filters_map['terrace'] == 'True' else "нет") + "</i>"

        if filters_map.get('hookah') is not None and filters_map['hookah'] == 'True':
            text += '\n' + "Есть кальян: <i>" + ("да" if filters_map['hookah'] == 'True' else "нет") + "</i>"
    else:
        text += "\n\nСейчас ты не применил никаких фильтров, но ты можешь сделать это в любой момент!"
    return text
