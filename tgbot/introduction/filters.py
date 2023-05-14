from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery

from tgbot.places.find_place import show_places
from tgbot.utils import states, values
from tgbot.introduction import keyboards
from tgbot.introduction.states import IntroStates


async def set_filters(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(call.message.chat.id, call.message.id)
    user_id = str(call.from_user.id)
    states.set_state(IntroStates.Filters, user_id)
    text = "Выбери нужные параметры для заведения, которое ты хочешь посетить."
    filters_map = values.get_all_values_from_map('filters_map', user_id)

    if not filters_map:
        values.add_values_to_map('filters_map', {'vegan': str(False)}, str(user_id))
        values.add_values_to_map('filters_map', {'hookah': str(False)}, str(user_id))
        values.add_values_to_map('filters_map', {'business': str(False)}, str(user_id))
        filters_map = values.get_all_values_from_map('filters_map', user_id)

    else:
        if len(filters_map) > 3:
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

    vegan = filters_map['vegan'] == 'True'
    hookah = filters_map['hookah'] == 'True'
    business = filters_map['business'] == 'True'

    await bot.send_message(
        chat_id=call.message.chat.id,
        text=text,
        reply_markup=keyboards.filters(vegan, business, hookah)
    )


async def filter_kitchens(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(call.message.chat.id, call.message.id)
    user_id = str(call.from_user.id)
    states.set_state(IntroStates.Kitchens, str(user_id))
    data = call.data

    text = "Выберите кухню, в которую хотите сейчас сьесть"
    pos = 0
    kitchens = values.get_list('kitchens', user_id)
    map_kitchens = values.get_all_values_from_map('filters_map', user_id)

    if data == "drop":
        kitchens = []
        values.delete_list('kitchens', user_id)

    if map_kitchens.get('kitchens_pos') is not None:
        pos = int(map_kitchens.get('kitchens_pos'))

    if data == "next" or data == "back":
        if data == "next":
            pos += 10
        else:
            pos -= 10

    if call.data.find("name") != -1:
        name = data[len("name"):]
        if name not in kitchens:
            kitchens.append(name)
            values.add_value_to_list('kitchens', name, user_id)

    if kitchens:
        text += "\n\n Сейчас выбраны кухни: "
        for kitchen in kitchens:
            text += kitchen + " "

    if map_kitchens.get('kitchens_pos') is None:
        map_kitchens = {
            'kitchens_pos': '0'
        }
    else:
        map_kitchens = {
            'kitchens_pos': str(pos)
        }
    values.add_values_to_map('filters_map', map_kitchens, user_id)
    await bot.send_message(
        chat_id=call.message.chat.id,
        text=text,
        reply_markup=keyboards.show_kitchens(pos))


async def set_vegan(call: CallbackQuery, bot: AsyncTeleBot):
    await set_value('vegan', call, bot)


async def set_business(call: CallbackQuery, bot: AsyncTeleBot):
    await set_value('business', call, bot)


async def set_hookah(call: CallbackQuery, bot: AsyncTeleBot):
    await set_value('hookah', call, bot)


async def set_value(name: str, call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    filters_map = values.get_all_values_from_map('filters_map', user_id)
    val = not filters_map[name] == 'True'
    values.add_values_to_map('filters_map', {name: str(val)}, user_id)
    await set_filters(call, bot)


async def filter_mid_price(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(call.message.chat.id, call.message.id)
    user_id = str(call.from_user.id)
    states.set_state(IntroStates.MidPrice, str(user_id))
    data = call.data

    text = "Выберите какой вам требуется средний чек на человека"

    if data.find('price_') != -1:
        num = data[len('price_'):]
        values.add_values_to_map('filters_map', {"mid_price": str(num)}, user_id)

    if data == 'drop':
        values.delete_value_from_map('filters_map', 'mid_price', user_id)

    num = values.get_value_from_map('filters_map', 'mid_price', user_id)
    if num is not None:
        if int(num) <= 5000:
            text += "\n\nВы выбрали средний чек до: " + num + '₽'
        else:
            text += "\n\nВы выбрали средний чек от: " + num + '₽'

    await bot.send_message(
        chat_id=call.message.chat.id,
        text=text,
        reply_markup=keyboards.mid_price())


async def filter_rating(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(call.message.chat.id, call.message.id)
    user_id = str(call.from_user.id)
    states.set_state(IntroStates.Rating, str(user_id))
    data = call.data

    text = "Выберите рейтинг заведения: "

    if data.find('rating_') != -1:
        num = data[len('rating_'):]
        values.add_values_to_map('filters_map', {"rating": str(num)}, user_id)

    if data == 'drop':
        values.delete_value_from_map('filters_map', 'rating', user_id)

    num = values.get_value_from_map('filters_map', 'rating', user_id)
    if num is not None:
        text += "\n\nВы выбрали рейтинг от: " + num

    await bot.send_message(
        chat_id=call.message.chat.id,
        text=text,
        reply_markup=keyboards.rating())


async def msg_drop_filters(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(call.message.chat.id, call.message.id)
    user_id = str(call.from_user.id)
    state = states.get_state(user_id)
    values.set_value('last_state', str(state), user_id)
    states.set_state(IntroStates.DropFilters, str(user_id))
    text = "Ты точно хочешь сбросить все фильтры?"
    await bot.send_message(
        chat_id=call.message.chat.id,
        text=text,
        reply_markup=keyboards.drop_filters())


async def drop_filters(call: CallbackQuery, bot: AsyncTeleBot):
    await drop_filters_map(call)
    await return_from_drop(call, bot)


async def drop_filters_map(call: CallbackQuery):
    user_id = str(call.from_user.id)
    values.clean_map('filters_map', user_id)
    values.delete_list('kitchens', user_id)


async def return_from_drop(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    state = values.get_value('last_state', user_id)
    if state == "show_places":
        await show_places(
            call.message.chat.id,
            str(call.from_user.id),
            call.message.id,
            bot)
    if state == "filters":
        await set_filters(call, bot)
