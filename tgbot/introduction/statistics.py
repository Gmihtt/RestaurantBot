from datetime import datetime, timedelta

from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery

from tgbot.introduction import keyboards
from tgbot.introduction.collection import user_collection, stat_collection
from tgbot.utils import states, functions, values
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
        user_count = user_collection.users_stat(cur_date - timedelta(hours=1))
        period = "за последний час"
    if data == "stat_day":
        user_count = user_collection.users_stat(cur_date - timedelta(days=1))
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


async def deeplink(call: CallbackQuery, bot: AsyncTeleBot):
    await functions.delete_message(call.message.chat.id, call.message.id, bot)
    user_id = str(call.from_user.id)
    states.set_state(IntroStates.DeepLink, user_id)
    map_deeplink = values.get_all_values_from_map('deeplink', user_id)

    if call.data == "deeplink":
        codes = stat_collection.get_all_codes()
        str_codes = ""
        for code in codes:
            str_codes += code + ','
        pos = 0
        v = {
            'codes': str_codes,
            'pos': str(pos)
        }
        values.add_values_to_map('deeplink', v, user_id)
    else:
        codes = map_deeplink['codes'].split(',')[:-1]
        pos = int(map_deeplink['pos'])
        v = {
            'pos': str(pos + 10)
        }
        values.add_values_to_map('deeplink', v, user_id)

    if call.data.find("code") != -1:
        code = call.data[len('code'):]
        stat = stat_collection.get_stat_by_code(code)
        user_ids = stat['user_ids']
        cur_date = datetime.now()
        users_count = len(user_ids)
        users_count_activity = user_collection.users_stat(cur_date - timedelta(days=30), user_ids)
        users_disable = users_count - users_count_activity
        text = f"{code} - Всего: {users_count}, Активных: {users_count_activity}, Неактивны: {users_disable}"
        await bot.send_message(text=text, chat_id=call.message.chat.id)

    if call.data == "next":
        pos += 10
    if call.data == "back":
        pos -= 10

    await bot.send_message(text="Список диплинков:",
                           chat_id=call.message.chat.id,
                           reply_markup=keyboards.show_deeplink_stat(codes, pos)
                           )


async def show_stat_by_cities(call: CallbackQuery, bot: AsyncTeleBot):
    await functions.delete_message(call.message.chat.id, call.message.id, bot)
    user_id = str(call.from_user.id)
    states.set_state(IntroStates.Cities, user_id)
    data = call.data
    if data == "cities":
        await bot.send_message(text="выберите город",
                               chat_id=call.message.chat.id,
                               reply_markup=keyboards.show_cities())
    else:
        cur_date = datetime.now()
        last_users = user_collection.users_stat(time=cur_date - timedelta(days=30), city=data)
        all_users = user_collection.users_stat(time=cur_date - timedelta(days=365 * 10), city=data)
        await bot.send_message(
            chat_id=call.message.chat.id,
            text=f"в городе {data}\n"
                 f"количество людей за последние 30 дней: {last_users}\n"
                 f"количество людей за все время: {all_users}"
        )
        await show_statistics(call, bot)
