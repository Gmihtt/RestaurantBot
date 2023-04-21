from typing import List

from telebot.async_telebot import AsyncTeleBot
from telebot.types import InputMediaPhoto, InputMediaVideo, Message

from tgbot import common_keyboards
from tgbot.common_types import File, FileTypes
from tgbot.config import main_admins
from tgbot.databases.database import db
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
    print(type_of_file)
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
