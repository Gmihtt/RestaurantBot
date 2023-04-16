from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery

from tgbot.utils import states
from tgbot.config import support, main_admins
from tgbot.databases.database import db
from tgbot.introduction import keyboards
from tgbot.introduction.states import IntroStates
from tgbot.types import User
from tgbot import common_keyboards


async def check_welcome(message: Message, bot: AsyncTeleBot):
    user_id = message.from_user.id
    states.set_state(IntroStates.Welcome, str(user_id))
    user = User(
        _id=None,
        user_tg_id=user_id,
        chat_id=message.chat.id,
        username=message.from_user.username
    )
    db.add_user(user)
    if user_id in main_admins or db.is_admin(user_id):
        await bot.reply_to(message, """
Выберете интерфейс
""", reply_markup=common_keyboards.show_admins_chose_buttons())
    else:
        await send_welcome(message, bot)


async def send_welcome(message: Message, bot: AsyncTeleBot):
    await bot.reply_to(message, """
Пришли мне свое местоположение и я покажу какие места есть рядом с тобой
Лучше всего делать это с телефона
""", reply_markup=keyboards.show_location_button())


async def send_welcome_callback(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.send_message(chat_id=call.message.chat.id, text="""
Пришли мне свое местоположение и я покажу какие места есть рядом с тобой
    """, reply_markup=keyboards.show_location_button())


async def show_admin_menu(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = call.from_user.id
    states.set_state(IntroStates.AdminMenu, str(user_id))
    await bot.delete_message(call.message.chat.id, call.message.id)
    await bot.send_message(chat_id=call.message.chat.id, text="""
    Основное меню:
    """, reply_markup=keyboards.show_admin_menu(call.from_user.id))


async def send_help(message: Message, bot: AsyncTeleBot):
    user_id = message.from_user.id
    states.set_state(IntroStates.Help, str(user_id))
    await bot.send_message(chat_id=message.chat.id, text="""
Кажется Вы ввели какое-то странное сообщение, либо Вам нужна помощь.\n
Если Вам нужна помощь, то напишите: """ + support + """\n
А если вы хотите найти место, то пришлите мне точку через телеграм
""")
