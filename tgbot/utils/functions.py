from typing import List

from telebot.async_telebot import AsyncTeleBot
from telebot.types import InputMediaPhoto, InputMediaVideo

from tgbot.config import main_admins
from tgbot.types import FileTypes, File
from tgbot.databases.database import db


def is_admin(user_id: str) -> bool:
    return user_id in main_admins or db.is_admin(user_id)


async def send_files(text: str,
                     chat_id: int,
                     files: List[File],
                     bot: AsyncTeleBot):
    if len(files) == 0:
        await bot.send_message(chat_id=chat_id, text=text)
    if len(files) == 1:
        file_type = files[0]['file']
        file_id = files[0]['file_id']
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
            file_type = files[0]['file']
            file_id = files[0]['file_id']
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
