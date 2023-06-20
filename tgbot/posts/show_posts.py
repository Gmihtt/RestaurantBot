from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery

from tgbot.databases.database import db
from tgbot.posts.pretty_show import pretty_show_post
from tgbot.utils import states, functions
from tgbot.posts.states import PostStates
from tgbot.posts import keyboards


async def find_posts_message(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = str(call.from_user.id)
    states.set_state(PostStates.Find, user_id)
    await functions.delete_message(call.message.chat.id, call.message.id, bot)
    await bot.send_message(chat_id=call.message.chat.id, text="""
        Последние 10 постов
        """, reply_markup=keyboards.chose_post_find_option(db.get_posts()))


async def send_post_info(call: CallbackQuery, bot: AsyncTeleBot):
    await functions.delete_message(call.message.chat.id, call.message.id, bot)
    user_id = str(call.from_user.id)
    states.set_state(PostStates.Show, user_id)
    post_id = call.data[len("post_id"):]
    post = db.find_post_by_id(post_id)
    if post is None:
        await bot.send_message(chat_id=call.message.chat.id, text="""
                Не вышло найти пост
                """)
    else:
        await bot.send_message(chat_id=call.message.chat.id, text=pretty_show_post(post))
