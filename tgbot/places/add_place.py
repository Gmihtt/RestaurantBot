import logging
from typing import Tuple, Optional

from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, Message

from tgbot.config import support
from tgbot.keyboard import keyboard
from tgbot.types.types import PlaceType, FileTypes, Place, Restaurant
from tgbot.databases.database import storage, db
from tgbot.utils.functions import pretty_show_place, send_files


async def place_example(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    storage.add('admin_place_info' + user_id, "wait")
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
                               text=f"""вы прислали {size} полей, а я ожидаю 6 как в примере, попробуйте заполнить сообщение еще раз""",
                               )
        return
    if check_coords(fields[2]):
        await bot.send_message(chat_id=message.chat.id,
                               text="""место с такими координатами уже существует\n"""
                                    """попробуйте заполнить еще раз, либо напишите: """ + support,
                               reply_markup=keyboard.show_admins_chose_buttons())
        return
    storage.delete('admin_place_info' + user_id)
    storage.add('admin_place_name' + user_id, fields[0])
    storage.add('admin_place_address' + user_id, fields[1])
    storage.add('admin_place_coords' + user_id, fields[2])
    storage.add('admin_place_phone' + user_id, fields[3])
    storage.add('admin_place_url' + user_id, fields[4])
    storage.add('admin_place_work' + user_id, fields[5])
    await bot.send_message(chat_id=message.chat.id,
                           text=f"""выберите какой это тип заведения""",
                           reply_markup=keyboard.show_all_places_type())


async def place_type_parse(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    user_id = str(call.from_user.id)
    if call.data == "place_type" + PlaceType.RESTAURANT.value:
        storage.add('admin_place_type' + user_id, PlaceType.RESTAURANT.value)
        await place_send_restaurant_message(call, bot)


async def place_send_restaurant_message(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    storage.add('admin_restaurant_info' + user_id, "wait")
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
                               text=f"вы прислали {size} полей, а я ожидаю 6 как в примере, попробуйте заполнить сообщение еще раз")
        return
    storage.delete('admin_restaurant_info' + user_id)
    storage.add('admin_restaurant_mid_price' + user_id, fields[0])
    storage.add('admin_restaurant_business_lunch' + user_id, fields[1])
    storage.add('admin_restaurant_business_lunch_price' + user_id, fields[2])
    storage.add('admin_restaurant_kitchen' + user_id, fields[3])
    storage.add('admin_place_files_count' + user_id, "0")
    await bot.send_message(chat_id=message.chat.id,
                           text="""Хотите ли вы добавить еще фото, видео или файл?""",
                           reply_markup=keyboard.show_add_photo(suffix="place"))


async def place_file_message(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(call.message.chat.id, call.message.id)
    await bot.send_message(chat_id=call.message.chat.id,
                           text="""Отправь мне до 10 медиа, которые хотите добавить к посту\n"""
                                """Лучше отправлять по одному сообщению""")


async def place_parse_file(message: Message, bot: AsyncTeleBot):
    user_id = str(message.from_user.id)
    logging.info(message.content_type)
    type_of_file = message.content_type
    if message.content_type == "photo":
        file = message.photo[0]
    else:
        file = message.video
    count = int(storage.get('admin_place_files_count' + user_id))
    if count >= 10:
        await bot.send_message(chat_id=message.chat.id,
                               text="""Вы прислали больше 10 вложений""")
        return
    storage.add('admin_place_files_count' + user_id, str(count + 1))
    if count == 0:
        storage.add('admin_place_files' + user_id, file.file_id + ';' + type_of_file)
    else:
        file_ids = storage.get('admin_place_files' + user_id)
        storage.add('admin_place_files' + user_id, file_ids + ',' + file.file_id + ';' + type_of_file)
    await bot.send_message(chat_id=message.chat.id,
                           text="""Хотите ли вы добавить еще фото или видео?""",
                           reply_markup=keyboard.show_add_photo(suffix="place"))


async def place_description_msg(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    user_id = str(call.from_user.id)
    storage.add('admin_place_description' + user_id, "wait")
    await bot.send_message(chat_id=call.message.chat.id,
                           text="""Пришлите мне описание места, одним текстовым сообщением""")


async def place_city_chose(message: Message, bot: AsyncTeleBot):
    user_id = str(message.from_user.id)
    storage.add('admin_place_description' + user_id, message.text)
    storage.add('admin_place_city' + user_id, "wait")
    await bot.send_message(chat_id=message.chat.id,
                           text="""Выберите город для которого заполняете это место""",
                           reply_markup=keyboard.show_all_cities(db.get_all_cities()))


def get_place_from_storage(data: str, user_id: str, getter) -> Optional[Place]:
    def make_files():
        vals = getter('admin_place_files' + user_id).split(',')
        ids_types = []
        for val in vals:
            file_id, file_type = tuple(val.split(';'))
            if file_type == 'photo':
                ids_types.append((file_id, FileTypes.Photo))
            elif file_type == 'video':
                ids_types.append((file_id, FileTypes.Video))
        return ids_types

    name = getter('admin_place_name' + user_id)
    city = data[len("city_id"):]
    address = getter('admin_place_address' + user_id)
    coordinates: Tuple[float, float] = tuple(map(float, getter('admin_place_coords' + user_id).split(',')))
    phone = getter('admin_place_phone' + user_id)
    url = getter('admin_place_url' + user_id)
    work_int = getter('admin_place_work' + user_id)
    place_type = PlaceType[getter('admin_place_type' + user_id)]
    description = getter('admin_place_description' + user_id)
    print("hello")
    file_ids_types = make_files()
    print("hello1")
    place = None
    if place_type == PlaceType.RESTAURANT:
        mid_price = getter('admin_restaurant_mid_price' + user_id)
        if mid_price == "нет":
            mid_price = None
        business_lunch = getter('admin_restaurant_business_lunch' + user_id)
        business_lunch = business_lunch == "да"
        business_lunch_price = getter('admin_restaurant_business_lunch_price' + user_id)
        if business_lunch_price == "нет":
            mid_price = None
        kitchen = getter('admin_restaurant_kitchen' + user_id)
        if kitchen == "нет":
            mid_price = None
        place = Place(
            _id=None,
            name=name,
            address=address,
            city=city,
            coordinates=coordinates,
            telephone=phone,
            url=url,
            work_interval=work_int,
            description=description,
            place_type=PlaceType.RESTAURANT,
            place=Restaurant(
                mid_price=mid_price,
                business_lunch=business_lunch,
                business_lunch_price=business_lunch_price,
                kitchen=kitchen
            ),
            last_modify_id=int(user_id),
            files=file_ids_types
        )
    return place


async def place_approve(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    user_id = str(call.from_user.id)
    storage.delete('admin_place_city' + user_id)
    place = get_place_from_storage(data=call.data,
                                   user_id=user_id,
                                   getter=storage.get)
    chat_id = call.message.chat.id
    await bot.send_message(chat_id=chat_id,
                           text="""пользователи увидят такое место, если вы его добавите""")
    await send_files(text=pretty_show_place(place, is_admin=True),
                     chat_id=chat_id,
                     files=place['files'],
                     bot=bot)
    await bot.send_message(chat_id=chat_id, reply_markup=keyboard.approve_place(), text="Выберите")


async def push_place(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    place = get_place_from_storage(data=call.data,
                                   user_id=str(call.from_user.id),
                                   getter=storage.get)
    place_id = db.add_place(place)
    chat_id = call.message.chat.id
    await bot.send_message(chat_id=chat_id,
                           text=f"Место добавлено и вот его id: {place_id}",
                           reply_markup=keyboard.button_admin_menu())