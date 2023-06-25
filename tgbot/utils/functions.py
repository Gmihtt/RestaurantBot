from typing import List

import mpu
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InputMediaPhoto, InputMediaVideo, Message

from tgbot import common_keyboards
from tgbot.common_types import File, FileTypes
from tgbot.config import main_admins, max_distance
from tgbot.databases.database import db
from tgbot.places.collection import place_collection
from tgbot.places.place import Coordinates
from tgbot.utils import values


def is_admin(user_id: str) -> bool:
    return user_id in main_admins or db.is_admin(user_id)


async def send_files(text: str,
                     chat_id: int,
                     files: List[File],
                     bot: AsyncTeleBot):
    if len(files) == 0:
        return await bot.send_message(chat_id=chat_id, text=text)
    if len(files) == 1:
        file_type = files[0]['file']
        file_id = files[0]['file_id']
        if file_type == FileTypes.Photo:
            return await bot.send_photo(chat_id=chat_id,
                                        caption=text,
                                        photo=file_id)
        if file_type == FileTypes.Video:
            return await bot.send_video(chat_id=chat_id,
                                        caption=text,
                                        video=file_id)
    else:
        list_of_medias = []
        for i, file in enumerate(files):
            file_type = file['file']
            file_id = file['file_id']
            if file_type == FileTypes.Photo:
                list_of_medias.append(
                    InputMediaPhoto(media=file_id, caption=text if i == 0 else None)
                )
            if file_type == FileTypes.Video:
                list_of_medias.append(
                    InputMediaVideo(media=file_id, caption=text if i == 0 else None)
                )
        return await bot.send_media_group(chat_id=chat_id,
                                          media=list_of_medias)


async def parse_file(message: Message, bot: AsyncTeleBot, suffix: str):
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
        file=FileTypes(type_of_file)
    )
    values.add_file_to_list(file=file, user_id=user_id)
    await bot.send_message(chat_id=message.chat.id,
                           text="""Хотите ли вы добавить еще фото или видео?""",
                           reply_markup=common_keyboards.show_file(suffix))


def count_distance(crds1: Coordinates, crds2: Coordinates):
    return mpu.haversine_distance(
        (crds1['latitude'], crds1['longitude']),
        (crds2['latitude'], crds2['longitude'])
    )


def count_relevant_places(user_id: str, crds: Coordinates):
    places = place_collection.find_close_place(crds, user_id, skip=0, limit=0)
    count = 0
    for place in places:
        if count_distance(crds, place['coordinates']) <= max_distance:
            count += 1
    return count


async def delete_message(chat_id: int, msg_id: int, bot: AsyncTeleBot):
    try:
        await bot.delete_message(chat_id, msg_id)
    except Exception:
        return


async def delete_old_msg(chat_id: int, bot: AsyncTeleBot):
    m_id = values.get_value('msg_id_delete', str(chat_id))
    if m_id is not None:
        await delete_message(chat_id, int(m_id), bot)
        values.delete_value('msg_id_delete', str(chat_id))


def create_metre_str(metre: int):
    if 11 <= metre % 100 <= 19:
        return str(metre) + ' метров'
    if metre % 10 == 0:
        return str(metre) + ' метров'
    if metre % 10 == 1:
        return str(metre) + ' метр'
    if 2 <= metre % 10 <= 4:
        return str(metre) + ' метра'
    if 5 <= metre % 10 <= 9:
        return str(metre) + ' метров'


def place_count_str(count: int):
    if 11 <= count % 100 <= 19:
        return str(count) + ' заведений'
    if count % 10 == 0:
        return str(count) + ' заведений'
    if count % 10 == 1:
        return str(count) + ' заведение'
    if 2 <= count % 10 <= 4:
        return str(count) + ' заведения'
    if 5 <= count % 10 <= 9:
        return str(count) + ' заведений'


def add_hookah_to_features():
    places = place_collection.find_all_places()
    for place in places:
        if "lounge" in place['place_types'] and place.get('place') is not None:
            if "Кальян-бар" not in place['place']['features']:
                place['place']['features'].append("Кальян-бар")
                place_collection.update_place(place)
