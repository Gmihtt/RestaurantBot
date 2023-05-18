from typing import Optional, List

from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, Message

from tgbot.common_types import File
from tgbot import common_keyboards
from tgbot.places import keyboards
from tgbot.places.collection import place_collection
from tgbot.places.place import PlaceType, Restaurant, Place
from tgbot.places.pretty_show import pretty_show_place
from tgbot.utils.functions import send_files, parse_file
from tgbot.places.states import PlaceStates
from tgbot.utils import states, values


async def place_search_message(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    states.set_state(PlaceStates.Search, user_id)
    await functions.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=call.message.chat.id,
                           text="""Заполни по шаблону информацию о месте, чтобы я мог его найти\n"""
                           """Пожалуйста, используйте только информацию из бота, в крайнем случае яндекса\n""")
    place_str = """
<Название>

<адрес> или <url> или <телефон>
"""
    await bot.send_message(chat_id=call.message.chat.id,
                           text=place_str)


async def place_search_parse(message: Message, bot: AsyncTeleBot):
    user_id = str(message.from_user.id)
    text = message.text
    fields = list(filter(lambda s: s != "", map(lambda s: s.strip(), text.split('\n'))))
    size = len(fields)
    if size != 2:
        await bot.send_message(chat_id=message.chat.id,
                               text=f"""вы прислали {size} полей, """
                                    """а я ожидаю 2 как в примере, попробуйте заполнить сообщение еще раз""",
                               )
        return

    place = place_collection.find_place({
            "name": fields[0],
            "address": fields[1]
        })
    if place is None:
        place = place_collection.find_place({
            "name": fields[0],
            "url": fields[1]
        })
    if place is None:
        place = place_collection.find_place({
            "name": fields[0],
            "phone": fields[1]
        })
    if place is None:
        await bot.send_message(chat_id=message.chat.id,
                               text=f"""Данные которые вы прислали не найдены, вероятно вы не так скопировали"""
                               )
        return
    else:
        values.add_values_to_map({"_id": str(place['_id'])}, user_id)
        await bot.send_message(chat_id=message.chat.id,
                               text="Место найдено")
        await place_send_restaurant_message(user_id, message.chat.id, bot)


async def place_send_restaurant_message(user_id: str, chat_id: int, bot: AsyncTeleBot):
    states.set_state(PlaceStates.AddRestaurantInfo, user_id)
    await bot.send_message(chat_id=chat_id,
                           text="""Заполни по шаблону информацию о ресторане""")
    place_str = """
<Средний чек заведения, либо напиши "нет">: 1000

<Есть ли бизнес ланч: да/нет>: да

<Стоимость бизнес ланча, либо напиши "нет">: 100

<Есть ли веганская еда: да/нет>: нет
"""
    await bot.send_message(chat_id=chat_id,
                           text=place_str)


async def place_restaurant_parse(message: Message, bot: AsyncTeleBot):
    user_id = str(message.from_user.id)
    text = message.text
    fields = list(filter(lambda s: s != "", map(lambda s: s.strip(), text.split('\n'))))
    size = len(fields)
    if size != 4:
        await bot.send_message(chat_id=message.chat.id,
                               text=f"""вы прислали {size} полей, """
                                    """а я ожидаю 4 как в примере, попробуйте заполнить сообщение еще раз""")
        return

    restaurant_info = {
        "mid_price": fields[0],
        "business_lunch": fields[1],
        "business_lunch_price": fields[2],
        "vegan": fields[3],
    }
    values.add_values_to_map(restaurant_info, user_id)
    await bot.send_message(chat_id=message.chat.id,
                           text="""Добавьте кухню""",
                           reply_markup=common_keyboards.show_all_kitchens())


async def add_kitchen(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    await functions.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    kitchen = call.data
    values.add_values_to_map({"kitchen": kitchen}, user_id)
    states.set_state(PlaceStates.AddFiles, user_id)
    await bot.send_message(chat_id=call.message.chat.id,
                           text="""Кухня добавлена\nХотите ли вы добавить еще фото или видео?""",
                           reply_markup=common_keyboards.show_file(suffix="place"))


async def place_file_message(call: CallbackQuery, bot: AsyncTeleBot):
    await functions.delete_message(call.message.chat.id, call.message.id)
    await bot.send_message(chat_id=call.message.chat.id,
                           text="""Отправь мне до 10 медиа, которые хотите добавить к посту\n"""
                                """Лучше отправлять по одному сообщению""")


async def place_parse_file(message: Message, bot: AsyncTeleBot):
    await parse_file(message, bot, "place")


async def place_description_msg(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    states.set_state(PlaceStates.AddDescription, user_id)
    await functions.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=call.message.chat.id,
                           text="""Пришлите мне описание места, одним текстовым сообщением""")


def get_place_from_storage(data: str, user_id: str, files: List[File]) -> Optional[Place]:
    place_map = values.get_all_values_from_map(user_id)
    place = place_collection.find_place_by_id(place_map['_id'])
    if place is None:
        return None

    if place['place_type'] == PlaceType.Restaurant:
        restaurant = Restaurant(
            mid_price=None if place_map['mid_price'] == "нет" else place_map['mid_price'],
            business_lunch=place_map['business_lunch'] == "да",
            business_lunch_price=
            None if place_map['business_lunch_price'] == "нет" else place_map['business_lunch_price'],
            kitchens=[place_map['kitchens']],
            vegan=place_map['vegan'] == "да",
        )
        place['place'] = restaurant
        place['description'] = data
        place['files'] = files
        return place


async def place_approve(message: Message, bot: AsyncTeleBot):
    user_id = str(message.from_user.id)
    states.set_state(PlaceStates.Approve, user_id)
    files = values.get_files(user_id)
    place = get_place_from_storage(data=message.text,
                                   user_id=user_id,
                                   files=files)
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id,
                           text="""пользователи увидят такое место, если вы его добавите\n""")
    await send_files(text=pretty_show_place(place),
                     chat_id=chat_id,
                     files=files,
                     bot=bot)
    await bot.send_message(chat_id=chat_id, reply_markup=keyboards.approve_place(), text="Выберите")


async def push_place(call: CallbackQuery, bot: AsyncTeleBot):
    await functions.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    user_id = str(call.from_user.id)
    states.set_state(PlaceStates.Approve, user_id)
    files = values.get_files(user_id)
    place = get_place_from_storage(data=call.data,
                                   user_id=str(call.from_user.id),
                                   files=files)
    place['last_modify_id'] = int(user_id)
    values.clean_map(user_id)
    values.delete_files(user_id)
    place_collection.update_place(place)
    chat_id = call.message.chat.id
    await bot.send_message(chat_id=chat_id,
                           text=f"Место обновлено",
                           reply_markup=common_keyboards.button_admin_menu())
