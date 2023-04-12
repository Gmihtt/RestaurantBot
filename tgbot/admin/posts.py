from datetime import datetime

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery, InputMediaPhoto

from tgbot.types.types import Post, pretty_show_post
from tgbot.utils.database import db, storage
import tgbot.keyboard.keyboard as keyboard


async def post_name_message(call: CallbackQuery, bot: AsyncTeleBot):
    if call.message is None:
        raise Exception("callback message is None")
    await bot.delete_message(call.message.chat.id, call.message.id)
    user_id = str(call.from_user.id)
    storage.add('admin_post_name' + user_id, "wait")
    await bot.send_message(chat_id=call.message.chat.id, text="""Пришли мне название поста""")


async def post_body_message(message: Message, bot: AsyncTeleBot):
    user_id = str(message.from_user.id)
    name = message.text
    storage.add('admin_post_name' + user_id, name)
    storage.add('admin_post_body' + user_id, "wait")
    await bot.send_message(chat_id=message.chat.id,
                           text="""Отправь мне текст поста""")


async def add_post_body(message: Message, bot: AsyncTeleBot):
    user_id = str(message.from_user.id)
    body = message.text
    storage.add('admin_post_body' + user_id, body)
    storage.add('admin_photo_count' + user_id, "0")
    await bot.send_message(chat_id=message.chat.id,
                           text="""Хотите ли вы добавить фото?""",
                           reply_markup=keyboard.show_add_photo(suffix="post"))


async def post_photo_message(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(call.message.chat.id, call.message.id)
    await bot.send_message(chat_id=call.message.chat.id,
                           text="""Отправь мне до 10 фото, которые хотите добавить к посту""")


async def add_post_photo(message: Message, bot: AsyncTeleBot):
    user_id = str(message.from_user.id)
    count = int(storage.get('admin_photo_count' + user_id))
    if count >= 10:
        await bot.send_message(chat_id=message.chat.id,
                               text="""Вы прислали больше 10 фото""")
        return
    storage.add('admin_photo_count' + user_id, str(count + 1))
    print(count)
    if count == 0:
        storage.add('admin_post_photos' + user_id, message.photo[0].file_id)
    else:
        file_ids = storage.get('admin_post_photos' + user_id)
        storage.add('admin_post_photos' + user_id, file_ids + ',' + message.photo[0].file_id)
    await bot.send_message(chat_id=message.chat.id,
                           text="""Хотите ли вы добавить еще фото?""",
                           reply_markup=keyboard.show_add_photo(suffix="post"))


async def approve_post_message(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(call.message.chat.id, call.message.id)
    user_id = str(call.from_user.id)
    chat_id = call.message.chat.id
    val = storage.get('admin_post_photos' + user_id)
    if val is None:
        file_ids = []
    else:
        file_ids = val.split(',')
    await bot.send_message(chat_id=chat_id, text="Вот что увидит пользователь:")
    body = storage.get('admin_post_body' + user_id)
    if len(file_ids) == 0:
        await bot.send_message(chat_id=chat_id, text=body, reply_markup=keyboard.approve_post())
    if len(file_ids) == 1:
        await bot.send_photo(chat_id=chat_id,
                             caption=body,
                             reply_markup=keyboard.approve_post(),
                             photo=file_ids[0])
    else:
        list_of_medias = []
        for i, file_id in enumerate(file_ids):
            list_of_medias.append(
                InputMediaPhoto(media=file_id, caption=body if i == 0 else None)
            )
        await bot.send_media_group(chat_id=chat_id,
                                   media=list_of_medias)
        await bot.send_message(chat_id=chat_id, reply_markup=keyboard.approve_post(), text="Выберите")


async def send_post(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    name = storage.pop('admin_post_name' + user_id)
    msg = storage.pop('admin_post_body' + user_id)
    file_ids = storage.pop('admin_post_photos' + user_id).split(',')

    all_users = db.get_all_users()
    count = 0
    for user in all_users:
        if user["_id"] != int(user_id):
            try:
                if len(file_ids) == 0:
                    await bot.send_message(chat_id=user["chat_id"], text=msg)
                elif len(file_ids) == 1:
                    await bot.send_photo(chat_id=user["chat_id"], caption=msg, photo=file_ids[0])
                else:
                    list_of_medias = []
                    for i, file_id in enumerate(file_ids):
                        list_of_medias.append(
                            InputMediaPhoto(media=file_id, caption=msg if i == 0 else None)
                        )
                    await bot.send_media_group(chat_id=user["chat_id"],
                                               media=list_of_medias)
            except BaseException as e:
                continue
            else:
                count += 1
    post = Post(
        _id=None,
        name=name,
        body=msg,
        count_users=count,
        user_id=int(user_id),
        date=datetime.now(),
        photos=file_ids
    )
    post_id = db.add_post(post)
    await bot.send_message(chat_id=call.message.chat.id, text=f"""Пост отправлен, его id: {post_id}""")


async def find_posts_message(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(call.message.chat.id, call.message.id)
    await bot.send_message(chat_id=call.message.chat.id, text="""
        Последние 10 постов
        """, reply_markup=keyboard.chose_post_find_option(db.get_posts()))


async def send_post_info(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(call.message.chat.id, call.message.id)
    post_id = call.data[len("post_id"):]
    print(post_id)
    post = db.find_post_by_id(post_id)
    if post is None:
        await bot.send_message(chat_id=call.message.chat.id, text="""
                Не вышло найти пост
                """)
    else:
        await bot.send_message(chat_id=call.message.chat.id, text=pretty_show_post(post))
