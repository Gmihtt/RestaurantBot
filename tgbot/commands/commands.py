from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from tgbot.types.types import Place, Restaurant, PlaceType
from tgbot.utils.database import Database, db

from tgbot.states.user_state import UserState


async def send_welcome(message: Message, bot: AsyncTeleBot):
    await bot.set_state(message.from_user.id, UserState.START, message.chat.id)
    print(db.find_close_place([2, 2], 1))
    await bot.reply_to(message, """
    Привет!\n
    Выбери место из списка любимых или группы, а еще можно найти новое с помощью поиска
    """)


async def send_help(message: Message, bot: AsyncTeleBot):
    await bot.set_state(message.from_user.id, UserState.HELP, message.chat.id)
    db.add_place(
        Place(
            name="test_name",
            city="test_city",
            place_type=PlaceType.RESTAURANT,
            place=Restaurant(
                menu="",
                mid_price=None,
                business_lunch=False,
                business_lunch_price=None,
                kitchen="china"
            ),
            address="addr",
            coordinates=(5.0, 5.0),
            photos=None,
            telephone="+79312075207",
            url=None,
            work_interval="17-20",
            description=None,
            last_modify_id=message.from_user.id
        )
    )
    await bot.reply_to(message, "help")
