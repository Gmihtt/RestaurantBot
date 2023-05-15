import asyncio

from telebot.async_telebot import AsyncTeleBot
from tgbot import config
from tgbot.common_types import File, FileTypes
from tgbot.places.collection import place_collection
import os


async def save_photos(bot: AsyncTeleBot):
    chat_id = 381873540
    path = config.photos_path
    places = os.listdir(path=path)
    for place_id in places:
        if place_id != ".DS_Store":
            path = config.photos_path + '/' + place_id
            photos = os.listdir(path=path)
            files = []
            place = place_collection.find_place_by_id(place_id)
            for photo_name in photos:
                if photo_name != ".DS_Store":
                    path = config.photos_path + '/' + place_id + '/' + photo_name
                    with open(path, "rb") as f:
                        photo = f.read()
                    message = await bot.send_photo(chat_id=chat_id, photo=photo)
                    os.remove(path)
                    files.append(
                        File(
                            file_id=message.photo[0].file_id,
                            file=FileTypes.Photo
                        )
                    )
                    await asyncio.sleep(1)
            os.rmdir(config.photos_path + '/' + place_id)
            if files:
                place['files'] = files
                place_collection.update_place(place)


