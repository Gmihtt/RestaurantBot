from datetime import datetime, timedelta

from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery

from tgbot.introduction import keyboards
from tgbot.introduction.collection import user_collection
from tgbot.utils import states, functions
from tgbot.introduction.states import IntroStates


async def show_statistics(call: CallbackQuery, bot: AsyncTeleBot):
    await functions.delete_message(call.message.chat.id, call.message.id, bot)
    user_id = call.from_user.id
    states.set_state(IntroStates.Statistics, str(user_id))
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="""Выберите какую статистику хотите получить""",
        reply_markup=keyboards.statistics()
    )


async def show_stat(call: CallbackQuery, bot: AsyncTeleBot):
    await functions.delete_message(call.message.chat.id, call.message.id, bot)
    data = call.data
    cur_date = datetime.now()
    user_count = 0
    period = ""
    if data == "stat_all":
        user_count = user_collection.users_count()
        period = "за все время"
    if data == "stat_hour":
        user_count = user_collection.users_stat(cur_date-timedelta(hours=1))
        period = "за последний час"
    if data == "stat_day":
        user_count = user_collection.users_stat(cur_date-timedelta(days=1))
        period = "за весь день"
    if data == "stat_week":
        user_count = user_collection.users_stat(cur_date - timedelta(days=7))
        period = "за всю неделю"
    if data == "stat_month":
        user_count = user_collection.users_stat(cur_date - timedelta(days=30))
        period = "за весь месяц"
    await bot.send_message(
        chat_id=call.message.chat.id,
        text=f"количество людей {period}: {user_count}"
    )
    await show_statistics(call, bot)

