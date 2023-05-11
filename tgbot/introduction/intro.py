from typing import Optional

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery

from tgbot.introduction import user
from tgbot.introduction.collection import user_collection
from tgbot.introduction.user import User
from tgbot.photos import save_photos
from tgbot.utils import states, values
from tgbot.config import main_admins
from tgbot.introduction import keyboards
from tgbot.introduction.states import IntroStates
from tgbot import common_keyboards


async def check_welcome(message: Message, bot: AsyncTeleBot):
    user_id = message.from_user.id
    states.set_state(IntroStates.Welcome, str(user_id))
    if user_id in main_admins: #or user_collection.is_admin(user_id):
        await bot.reply_to(message, """
Выберете интерфейс
""", reply_markup=common_keyboards.show_admins_chose_buttons())
    else:
        await send_welcome(message, bot)


intro_text = """
Привет!

Я  бот, который поможет тебе найти крутой ресторан, 
или атмосферное кафе для приятного время проведения в Москве, 
Санкт-Петербурге и Сочи прямо возле тебя!

Для использования нажми кнопку Найти место!

Если ты не ешь мясо, или хочешь определенную кухню, или, чтобы средний чек был до 1000 рублей, 
то жми на кнопку Параметры поиска и выставляй нужные фильтры!

Приятного время провождения!
"""


async def send_welcome(message: Message, bot: AsyncTeleBot):
    await welcome(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        username=message.from_user.username,
        bot=bot)


async def send_welcome_callback(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(call.message.chat.id, call.message.id)
    await welcome(
        user_id=call.from_user.id,
        chat_id=call.message.chat.id,
        username=call.from_user.username,
        bot=bot)


async def welcome(
        user_id: int,
        chat_id: int,
        username: Optional[str],
        bot: AsyncTeleBot):
    user_id = user_id
    states.set_state(IntroStates.MainMenu, str(user_id))
    u = await save_user(
        user_id=user_id,
        chat_id=chat_id,
        username=username
    )
    await bot.send_message(
        chat_id=chat_id,
        text=intro_text,
        reply_markup=keyboards.main_menu(favorites=u['favorites'] != [])
    )


async def save_user(user_id: int, chat_id: int, username: Optional[str]) -> User:
    u = user_collection.get_user_by_tg_id(user_id)
    if u is None:
        print("save user")
        u = user.User(
            _id=None,
            user_tg_id=user_id,
            chat_id=chat_id,
            username=username,
            city="",
            is_admin=False,
            favorites=[]
        )
        user_collection.add_user(u)
    return u


async def show_admin_menu(call: CallbackQuery, bot: AsyncTeleBot):
    await save_photos(bot)
    await bot.delete_message(call.message.chat.id, call.message.id)
    user_id = call.from_user.id
    states.set_state(IntroStates.AdminMenu, str(user_id))
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="""Основное меню:""",
        reply_markup=keyboards.show_admin_menu(call.from_user.id)
    )


async def place_preview(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(call.message.chat.id, call.message.id)
    user_id = str(call.from_user.id)
    text = """Чтобы подобрать для Вас рестораны, мне нужно точка, вокруг которой я буду искать заведения.\n
Вы можете прислать отдельную точку, либо нажать кнопку ниже, чтобы рестораны сразу возле тебя."""
    text_filter = await show_filters(user_id)
    text += text_filter
    message = await bot.send_message(
        chat_id=call.message.chat.id,
        text="Пришлите местоположение",
        reply_markup=keyboards.find_place()
    )
    values.set_value('loc_msg', str(message.id), user_id)
    await bot.send_message(
        chat_id=call.message.chat.id,
        text=text,
        reply_markup=keyboards.back_main_menu()
    )


async def show_filters(user_id: str):
    text = ""
    filters_map = values.get_all_values_from_map('filters_map', user_id)
    if filters_map:
        text += "\n\n" + "Фильтры, которые Вы выбрали: "
        kitchens = values.get_list('kitchens', user_id)
        if kitchens is not None and kitchens != []:
            text += '\n\n' + "Кухни: "
            for kitchen in kitchens:
                text += kitchen + " "

        if filters_map.get('mid_price') is not None:
            mid_price = int(filters_map['mid_price'])
            if mid_price <= 5000:
                text += '\n' + "Средний чек: до " + str(mid_price) + '₽'
            else:
                text += '\n' + "Средний чек: от " + str(5000) + '₽'

        if filters_map.get('rating') is not None:
            rating = filters_map['rating']
            text += '\n' + "Рейтинг от: " + rating

        if filters_map.get('business') is not None:
            text += '\n' + "Бизнес-ланч: " + ("да" if filters_map['business'] == 'True' else "нет")

        if filters_map.get('vegan') is not None:
            text += '\n' + "Веганское меню: " + ("да" if filters_map['vegan'] == 'True' else "нет")

        if filters_map.get('terrace') is not None:
            text += '\n' + "Летняя терраса: " + ("да" if filters_map['terrace'] == 'True' else "нет")

        if filters_map.get('hookah') is not None:
            text += '\n' + "Есть кальян: " + ("да" if filters_map['hookah'] == 'True' else "нет")
    else:
        text += """\n\nВ данный момент ты не применил никаких фильтров,
    если тебе это понадобится, ты всегда можно это сделать в основном меню."""
    return text
