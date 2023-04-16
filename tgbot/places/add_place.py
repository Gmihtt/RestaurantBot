from typing import Optional, List

from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, Message

from tgbot.common_types import FileTypes, File
from tgbot.config import support
from tgbot import common_keyboards
from tgbot.places import keyboards
from tgbot.places.place import PlaceType, Restaurant, Place
from tgbot.places.pretty_show import pretty_show_place
from tgbot.databases.database import db
from tgbot.utils.functions import send_files
from tgbot.places.states import PlaceStates
from tgbot.utils import states, values


async def place_example(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    states.set_state(PlaceStates.AddInfo, user_id)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=call.message.chat.id,
                           text="""Для начала заполни по шаблону информацию о месте""")
    place_str = """
<строка с названием места>

<адрес>

<коориданты выглядеть должны так, без пробелов и лишних символов: 37.580484,55.7486481>

<телефон>

<ссылка на место>

<рабочее время>
"""
    await bot.send_message(chat_id=call.message.chat.id,
                           text=place_str)


async def place_info_parse(message: Message, bot: AsyncTeleBot):
    def check_coords(str_coords: str):
        coords = tuple(map(float, str_coords.split(',')))
        places = db.find_close_place(coords, 0, 1)
        print(places)
        if places:
            return tuple(places[0]['coordinates']) == coords
        else:
            return False

    user_id = str(message.from_user.id)
    text = message.text
    fields = list(filter(lambda s: s != "", map(lambda s: s.strip(), text.split('\n'))))
    size = len(fields)
    if size != 6:
        await bot.send_message(chat_id=message.chat.id,
                               text=f"""вы прислали {size} полей, """
                                    """а я ожидаю 6 как в примере, попробуйте заполнить сообщение еще раз""",
                               )
        return
    if check_coords(fields[2]):
        await bot.send_message(chat_id=message.chat.id,
                               text="""место с такими координатами уже существует\n"""
                                    """попробуйте заполнить еще раз, либо напишите: """ + support,
                               reply_markup=common_keyboards.show_admins_chose_buttons())
        return

    place_info = {
        "name": fields[0],
        "address": fields[1],
        "coordinates": fields[2],
        "phone": fields[3],
        "url": fields[4],
        "work": fields[5]
    }
    values.add_values_to_map(place_info, user_id)
    await bot.send_message(chat_id=message.chat.id,
                           text=f"""выберите какой это тип заведения""",
                           reply_markup=keyboards.show_all_places_type())


async def place_type_parse(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    user_id = str(call.from_user.id)
    text = call.data[len("place_type"):]
    if text == PlaceType.Restaurant.value:
        states.set_state(PlaceStates.AddRestaurantInfo, user_id)
        place_type = {
            "place_type": PlaceType.Restaurant.value
        }
        values.add_values_to_map(place_type, user_id)
        await place_send_restaurant_message(call, bot)


async def place_send_restaurant_message(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.send_message(chat_id=call.message.chat.id,
                           text="""Заполни по шаблону информацию о ресторане""")
    place_str = """
<Средний чек заведения, либо напиши "нет">: 1000

<Есть ли бизнес ланч: да/нет>: да

<стоимость бизнес ланча, либо напиши "нет">: 100

<кухня, либо напиши "нет">: русская кухня/европейская
"""
    await bot.send_message(chat_id=call.message.chat.id,
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
        "kitchen": fields[3],
    }
    values.add_values_to_map(restaurant_info, user_id)
    await bot.send_message(chat_id=message.chat.id,
                           text="""Хотите ли вы добавить еще фото, видео или файл?""",
                           reply_markup=common_keyboards.show_file(suffix="place"))


async def place_file_message(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    states.set_state(PlaceStates.AddFiles, user_id)
    await bot.delete_message(call.message.chat.id, call.message.id)
    await bot.send_message(chat_id=call.message.chat.id,
                           text="""Отправь мне до 10 медиа, которые хотите добавить к посту\n"""
                                """Лучше отправлять по одному сообщению""")


async def place_parse_file(message: Message, bot: AsyncTeleBot):
    user_id = str(message.from_user.id)
    type_of_file = message.content_type
    if message.content_type == "photo":
        file_tg = message.photo[0]
    elif message.content_type == "video":
        file_tg = message.video
    else:
        file_tg = message.document

    count = values.get_count_files(user_id)
    if count >= 10:
        await bot.send_message(chat_id=message.chat.id,
                               text="""Вы прислали больше 10 вложений""")
        return
    file = File(
        file_id=file_tg.file_id,
        file=FileTypes[type_of_file]
    )
    values.add_file_to_list(file=file, user_id=user_id)
    await bot.send_message(chat_id=message.chat.id,
                           text="""Хотите ли вы добавить еще фото или видео?""",
                           reply_markup=common_keyboards.show_file(suffix="place"))


async def place_description_msg(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    states.set_state(PlaceStates.AddDescription, user_id)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=call.message.chat.id,
                           text="""Пришлите мне описание места, одним текстовым сообщением""")


async def place_city_chose(message: Message, bot: AsyncTeleBot):
    user_id = str(message.from_user.id)
    states.set_state(PlaceStates.AddCity, user_id)
    place_description = {
        "description": message.text
    }
    values.add_values_to_map(place_description, user_id)
    await bot.send_message(chat_id=message.chat.id,
                           text="""Выберите город для которого заполняете это место""",
                           reply_markup=keyboards.show_all_cities(db.get_all_cities()))


def get_place_from_storage(data: str, user_id: str, files: List[File]) -> Optional[Place]:
    place_map = values.get_all_values_from_map(user_id)
    city_id = data[len("city_id"):]
    l_coords = list(map(float, place_map['coordinates'].split(',')))
    coordinates = (l_coords[0], l_coords[1])
    place_type = PlaceType[place_map['place_type']]

    if place_type == PlaceType.Restaurant:
        restaurant = Restaurant(
            mid_price=None if place_map['mid_price'] == "нет" else place_map['mid_price'],
            business_lunch=place_map['business_lunch'] == "да",
            business_lunch_price=
            None if place_map['business_lunch_price'] == "нет" else place_map['business_lunch_price'],
            kitchen=None if place_map['kitchen'] == "нет" else place_map['kitchen'],
        )

        place = Place(
            _id=None,
            name=place_map['name'],
            address=place_map['address'],
            city_id=city_id,
            coordinates=coordinates,
            telephone=place_map['phone'],
            url=place_map['url'],
            work_interval=place_map['work'],
            description=place_map['description'],
            place_type=place_type.value,
            place=restaurant,
            last_modify_id=int(user_id),
            files=files
        )
        return place


async def place_approve(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    user_id = str(call.from_user.id)
    states.set_state(PlaceStates.Push, user_id)
    files = values.get_files(user_id)
    place = get_place_from_storage(data=call.data,
                                   user_id=user_id,
                                   files=files)
    chat_id = call.message.chat.id
    await bot.send_message(chat_id=chat_id,
                           text="""пользователи увидят такое место, если вы его добавите""")
    await send_files(text=pretty_show_place(place, is_admin=True),
                     chat_id=chat_id,
                     files=files,
                     bot=bot)
    await bot.send_message(chat_id=chat_id, reply_markup=keyboards.approve_place(), text="Выберите")


async def push_place(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    user_id = str(call.from_user.id)
    files = values.get_files(user_id)
    place = get_place_from_storage(data=call.data,
                                   user_id=str(call.from_user.id),
                                   files=files)
    values.delete_files(user_id)
    place_id = db.add_place(place)
    chat_id = call.message.chat.id
    await bot.send_message(chat_id=chat_id,
                           text=f"Место добавлено и вот его id: {place_id}",
                           reply_markup=common_keyboards.button_admin_menu())
