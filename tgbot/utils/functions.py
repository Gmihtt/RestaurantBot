from typing import List, Tuple, Optional

from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InputMediaPhoto, InputMediaVideo, InputMediaDocument

from tgbot.types.types import Place, Restaurant, PlaceType, FileTypes
from tgbot.utils.database import db


def pretty_show_restaurant(rest: Restaurant) -> str:
    mid_price = ""
    if rest['mid_price'] is not None:
        mid_price = 'средний чек: ' + str(rest['mid_price']) + '\n'
    business_lunch_price = ""
    if rest['business_lunch']:
        business_lunch_price = 'цена бизнес ланча: ' + str(rest['business_lunch_price']) + '\n'
    kitchen = ""
    if rest['kitchen'] is not None:
        kitchen = 'кухня: ' + rest['kitchen'] + '\n'
    return mid_price + business_lunch_price + kitchen


def pretty_show_place(place: Place, is_admin: bool) -> str:
    print(place)
    id = ""
    if place['_id'] is not None:
        id = "" if not is_admin else "id: " + str(place['_id']) + '\n'
    name = "Название: " + place['name'] + '\n'
    place_str = ""
    if place['place_type'] == PlaceType.RESTAURANT:
        place_str = pretty_show_restaurant(place['place']) + '\n'
    address = "Адресс" + place['address'] + '\n'
    telephone = "Телефон" + place['telephone'] + '\n'
    url = "" if place['url'] is None else place['url'] + '\n'
    work_interval = "Время работы: " + place['work_interval'] + '\n'
    description = "" if place['description'] is None else place['description'] + '\n'
    return (id +
            name +
            place_str +
            address +
            telephone +
            url +
            work_interval +
            description
            )


def generate_places(count: int):
    for i in range(count):
        place = Place(
            _id=None,
            name="name" + str(i),
            city="city" + str(i),
            place_type=PlaceType.RESTAURANT,
            place=Restaurant(
                mid_price=None,
                business_lunch=False,
                business_lunch_price=None,
                kitchen=None
            ),
            address="address" + str(i),
            coordinates=(i, i),
            telephone=str(i),
            url=None,
            work_interval="",
            description=None,
            last_modify_id=0,
            files=[]
        )
        db.add_place(place)


async def send_files(text: str,
                     chat_id: int,
                     files: List[Tuple[str, FileTypes]],
                     bot: AsyncTeleBot):
    if len(files) == 0:
        await bot.send_message(chat_id=chat_id, text=text)
    if len(files) == 1:
        file_type = files[0][1]
        file_id = files[0][0]
        if file_type == FileTypes.Photo:
            await bot.send_photo(chat_id=chat_id,
                                 caption=text,
                                 photo=file_id)
        if file_type == FileTypes.Video:
            await bot.send_video(chat_id=chat_id,
                                 caption=text,
                                 video=file_id)
    else:
        list_of_medias = []
        for i, file in enumerate(files):
            file_type = file[1]
            file_id = file[0]
            if file_type == FileTypes.Photo:
                list_of_medias.append(
                    InputMediaPhoto(media=file_id, caption=text if i == 0 else None)
                )
            if file_type == FileTypes.Video:
                list_of_medias.append(
                    InputMediaVideo(media=file_id, caption=text if i == 0 else None)
                )
        await bot.send_media_group(chat_id=chat_id,
                                   media=list_of_medias)
