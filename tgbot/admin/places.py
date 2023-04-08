from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, Message

from tgbot.keyboard.keyboard import show_all_cities, show_all_places_type, show_add_photo
from tgbot.types.types import PlaceType, FileTypes
from tgbot.utils.database import storage, db


async def place_example(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    storage.add('admin_place_info' + user_id, "wait")
    await bot.send_message(chat_id=call.message.chat.id,
                           text="""Для начала заполни по шаблону информацию о месте""")
    place_str = """
        <строка с названием места>

        <адрес>

        <коориданты выглядеть должны так: 55.7486481,37.580484>

        <телефон>

        <ссылка на место>

        <рабочее время>
    """
    await bot.send_message(chat_id=call.message.chat.id,
                           text=place_str)


async def place_info_parse(message: Message, bot: AsyncTeleBot):
    user_id = str(message.from_user.id)
    text = message.text
    fields = list(filter(lambda s: s != "", map(lambda s: s.strip(), text.split('\n'))))
    size = len(fields)
    if size != 6:
        await bot.send_message(chat_id=message.chat.id,
                               text=f"""вы прислали {size} полей, а я ожидаю 6 как в примере, попробуйте заполнить сообщение еще раз""",
                               )
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
                           reply_markup=show_all_places_type())


async def place_type_parse(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    if call.data == PlaceType.RESTAURANT.value:
        storage.add('admin_place_type' + user_id, PlaceType.RESTAURANT.value)
        await place_send_restaurant_message(call, bot)


async def place_send_restaurant_message(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    storage.add('admin_restaurant_info' + user_id, "wait")
    await bot.send_message(chat_id=call.message.chat.id,
                           text="""Заполни по шаблону информацию о ресторане""")
    place_str = """
            <Средний чек заведения, либо напиши "нет">

            <Есть ли бизнес ланч: да/нет>

            <стоимость бизнес ланча, либо напиши "нет">

            <кухня, либо напиши "нет">
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
    await bot.send_message(chat_id=message.chat.id,
                           text="""Хотите ли вы добавить еще фото или файл?""",
                           reply_markup=show_add_photo())


async def place_parse_file(message: Message, bot: AsyncTeleBot, type_of_file: str):
    user_id = str(message.from_user.id)
    if type_of_file == "document":
        file = message.document
    elif type_of_file == "photo":
        file = message.photo[0]
    else:
        file = message.video
    val = storage.get('admin_place_files_count' + user_id)
    if val is None:
        count = 0
    else:
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
                           text="""Хотите ли вы добавить еще фото или файл?""",
                           reply_markup=show_add_photo())


async def place_description_msg(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    storage.add('admin_place_description' + user_id, "wait")
    await bot.send_message(chat_id=call.message.chat.id,
                           text="""Пришлите мне описание места, одним текстовым сообщением""")


async def place_description_(message: Message, bot: AsyncTeleBot):
    user_id = str(message.from_user.id)
    description = message.text
    name = storage.get('admin_place_name' + user_id)
    storage.delete('admin_place_name' + user_id)
    address = storage.get('admin_place_address' + user_id)
    storage.delete('admin_place_address' + user_id)
    coords = storage.get('admin_place_coords' + user_id)
    storage.delete('admin_place_coords' + user_id)
    phone = storage.get('admin_place_phone' + user_id)
    storage.delete('admin_place_phone' + user_id)
    url = storage.get('admin_place_url' + user_id)
    storage.delete('admin_place_url' + user_id)
    work_int = storage.get('admin_place_work' + user_id)
    storage.delete('admin_place_work' + user_id)
    place_type = PlaceType[storage.get('admin_place_type' + user_id)]
    storage.delete('admin_place_type' + user_id)
    files
    if place_type == PlaceType.RESTAURANT:
        mid_price = storage.get('admin_restaurant_mid_price' + user_id)
        storage.delete('admin_restaurant_mid_price' + user_id)
        business_lunch = storage.add('admin_restaurant_business_lunch' + user_id)
        storage.delete('admin_restaurant_business_lunch' + user_id)
        business_lunch_price = storage.add('admin_restaurant_business_lunch_price' + user_id)
        storage.delete('admin_restaurant_business_lunch_price' + user_id)
        kitchen = storage.add('admin_restaurant_kitchen' + user_id)
        storage.delete('admin_restaurant_kitchen' + user_id)
