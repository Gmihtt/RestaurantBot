from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery

from tgbot.places.find_place import show_places
from tgbot.places.place import Coordinates, PlaceType
from tgbot.places.pretty_show import pretty_show_place_type
from tgbot.utils import states, values, functions
from tgbot.introduction import keyboards
from tgbot.introduction.states import IntroStates


async def set_filters(call: CallbackQuery, bot: AsyncTeleBot):
    await functions.delete_message(call.message.chat.id, call.message.id, bot)
    user_id = str(call.from_user.id)
    states.set_state(IntroStates.Filters, user_id)
    text = "Выбери какой формат заведения подойдет тебе!"
    filters_map = values.get_all_values_from_map('filters_map', user_id)

    if not filters_map:
        values.add_values_to_map('filters_map', {'vegan': str(False)}, str(user_id))
        values.add_values_to_map('filters_map', {'hookah': str(False)}, str(user_id))
        values.add_values_to_map('filters_map', {'business': str(False)}, str(user_id))
        filters_map = values.get_all_values_from_map('filters_map', user_id)

    else:
        if len(filters_map) > 3:
            text += "\n\n" + "Выбранные фильтры: "
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

    vegan = filters_map['vegan'] == 'True'
    hookah = filters_map['hookah'] == 'True'
    business = filters_map['business'] == 'True'

    await bot.send_message(
        chat_id=call.message.chat.id,
        text=text,
        reply_markup=keyboards.filters(vegan, business, hookah),
        parse_mode="html"
    )


async def filter_kitchens(call: CallbackQuery, bot: AsyncTeleBot):
    await functions.delete_message(call.message.chat.id, call.message.id, bot)
    user_id = str(call.from_user.id)
    states.set_state(IntroStates.Kitchens, str(user_id))
    data = call.data

    text = "Выбери наиболее предпочтительную кухню!"
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
        text += "\n\nТы выбрал кухни: <i>"
        for kitchen in kitchens:
            text += kitchen + " "
        text += "</i>"

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
        reply_markup=keyboards.show_kitchens(pos),
        parse_mode="html"
    )


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
    await functions.delete_message(call.message.chat.id, call.message.id, bot)
    user_id = str(call.from_user.id)
    states.set_state(IntroStates.MidPrice, str(user_id))
    data = call.data

    text = "Выбери средний чек!"

    if data.find('price_') != -1:
        num = data[len('price_'):]
        values.add_values_to_map('filters_map', {"mid_price": str(num)}, user_id)

    if data == 'drop':
        values.delete_value_from_map('filters_map', 'mid_price', user_id)

    num = values.get_value_from_map('filters_map', 'mid_price', user_id)
    if num is not None:
        text += "\n\nТы выбрал средний чек от: <i>" + num + '₽</i>'

    await bot.send_message(
        chat_id=call.message.chat.id,
        text=text,
        reply_markup=keyboards.mid_price(),
        parse_mode="html"
    )


async def filter_rating(call: CallbackQuery, bot: AsyncTeleBot):
    await functions.delete_message(call.message.chat.id, call.message.id, bot)
    user_id = str(call.from_user.id)
    states.set_state(IntroStates.Rating, user_id)
    data = call.data

    text = "Выбери рейтинг заведения!"

    if data.find('rating_') != -1:
        num = data[len('rating_'):]
        values.add_values_to_map('filters_map', {"rating": str(num)}, user_id)

    if data == 'drop':
        values.delete_value_from_map('filters_map', 'rating', user_id)

    num = values.get_value_from_map('filters_map', 'rating', user_id)
    if num is not None:
        text += "\n\nТы выбрал рейтинг от: <i>" + num + "</i>"

    await bot.send_message(
        chat_id=call.message.chat.id,
        text=text,
        reply_markup=keyboards.rating(),
        parse_mode="html"
    )


async def filter_place_type(call: CallbackQuery, bot: AsyncTeleBot):
    await functions.delete_message(call.message.chat.id, call.message.id, bot)
    user_id = str(call.from_user.id)
    states.set_state(IntroStates.PlaceTypes, user_id)
    data = call.data
    text = "Выбери какой формат заведения тебе нужен!"

    if data == 'drop':
        values.delete_list('place_types', user_id)
    elif data != 'place_types':
        p_t = values.get_list('place_types', user_id)
        if p_t is not None and data not in p_t:
            values.add_value_to_list('place_types', data, user_id)
        if p_t is None:
            values.add_value_to_list('place_types', data, user_id)

    place_types = values.get_list('place_types', user_id)
    if place_types is not None:
        text += "\n\nТы выбрала заведения такого типа: <i>"
        for p_t in place_types:
            text += pretty_show_place_type(PlaceType(p_t)) + " "
        text += "</i>"

    await bot.send_message(
        chat_id=call.message.chat.id,
        text=text,
        reply_markup=keyboards.show_place_type(),
        parse_mode="html"
    )


async def msg_drop_filters(call: CallbackQuery, bot: AsyncTeleBot):
    await functions.delete_message(call.message.chat.id, call.message.id, bot)
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
    values.delete_list('place_types', user_id)


async def return_from_drop(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    state = values.get_value('last_state', user_id)
    if state == "show_places":
        position = values.get_all_values_from_map('place_map', user_id)
        loc = position.get('location')
        if loc is not None:
            new_loc = loc.split(",")
            crds = Coordinates(
                longitude=float(new_loc[0]),
                latitude=float(new_loc[1])
            )
            count = functions.count_relevant_places(user_id, crds)
            values.add_values_to_map('place_map', {'count': str(count)}, user_id)

        await show_places(
            call.message.chat.id,
            str(call.from_user.id),
            call.message.id,
            bot)
    if state == "filters":
        await set_filters(call, bot)
