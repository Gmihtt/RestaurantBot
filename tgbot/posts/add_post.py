from datetime import datetime

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery

from tgbot.databases.database import db
from tgbot.utils import states
from tgbot.utils import values
from tgbot.posts.states import PostStates
from tgbot.posts import keyboards
from tgbot import common_keyboards
from tgbot.posts.post import Post
from tgbot.utils.functions import parse_file, send_files


async def post_name_message(call: CallbackQuery, bot: AsyncTeleBot):
    if call.message is None:
        raise Exception("callback message is None")
    await bot.delete_message(call.message.chat.id, call.message.id)
    user_id = str(call.from_user.id)
    states.set_state(PostStates.Name, user_id)
    await bot.send_message(chat_id=call.message.chat.id, text="""Пришли мне название поста""")


async def post_body_message(message: Message, bot: AsyncTeleBot):
    user_id = str(message.from_user.id)
    states.set_state(PostStates.Body, user_id)
    name = message.text
    post = {
        "name": name
    }
    values.add_values_to_map(post, user_id)
    await bot.send_message(chat_id=message.chat.id,
                           text="""Отправь мне текст поста""")


async def add_post_body(message: Message, bot: AsyncTeleBot):
    user_id = str(message.from_user.id)
    states.set_state(PostStates.Files, user_id)
    body = message.text
    post = {
        "body": body
    }
    values.add_values_to_map(post, user_id)
    await bot.send_message(chat_id=message.chat.id,
                           text="""Хотите ли вы добавить фото?""",
                           reply_markup=common_keyboards.show_file(suffix="post"))


async def post_file_message(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(call.message.chat.id, call.message.id)
    await bot.send_message(chat_id=call.message.chat.id,
                           text="""Отправь мне до 10 фото, которые хотите добавить к посту""")


async def add_post_file(message: Message, bot: AsyncTeleBot):
    await parse_file(message, bot, "post")


async def approve_post_message(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(call.message.chat.id, call.message.id)
    user_id = str(call.from_user.id)
    states.set_state(PostStates.Approve, user_id)
    chat_id = call.message.chat.id
    files = values.get_files(user_id)
    post = values.get_all_values_from_map(user_id)
    await bot.send_message(chat_id=chat_id, text="Вот что увидит пользователь:")
    await send_files(text=post["body"],
                     chat_id=chat_id,
                     files=files,
                     bot=bot)
    await bot.send_message(chat_id=chat_id, reply_markup=keyboards.approve_post(), text="Выберите")


async def send_post(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    states.set_state(PostStates.Push, user_id)
    post = values.get_all_values_from_map(user_id)
    files = values.get_files(user_id)
    values.delete_files(user_id)

    all_users = db.get_all_users()
    count = 0
    for user in all_users:
        if user["_id"] != int(user_id):
            try:
                await send_files(text=post["body"],
                                 chat_id=user["chat_id"],
                                 files=files,
                                 bot=bot)
            except BaseException as e:
                continue
            else:
                count += 1
    post = Post(
        _id=None,
        name=post['name'],
        body=post['body'],
        count_users=count,
        user_id=int(user_id),
        date=datetime.now(),
        files=files
    )
    post_id = db.add_post(post)
    await bot.send_message(chat_id=call.message.chat.id, text=f"""Пост отправлен, его id: {post_id}""")
