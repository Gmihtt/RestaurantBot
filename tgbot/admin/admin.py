import logging
from datetime import datetime
from typing import Optional

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery

from tgbot.config import support, main_admins
from tgbot.types.types import pretty_show_place, Post, pretty_show_post
from tgbot.utils.database import db, storage
import tgbot.keyboard.keyboard as keyboard


async def show_admin_menu(call: CallbackQuery, bot: AsyncTeleBot):
    await bot.delete_message(call.message.chat.id, call.message.id)
    await bot.send_message(chat_id=call.message.chat.id, text="""
    Основное меню:
    """, reply_markup=keyboard.show_admin_menu(call.from_user.id))


async def add_post_name_message(call: CallbackQuery, bot: AsyncTeleBot):
    if call.message is None:
        raise Exception("callback message is None")
    await bot.delete_message(call.message.chat.id, call.message.id)
    user_id = str(call.from_user.id)
    storage.add('admin_post' + user_id, "name")
    await bot.send_message(chat_id=call.message.chat.id, text="""Пришли мне название поста""")


async def add_post_body_message(message: Message, bot: AsyncTeleBot):
    user_id = str(message.from_user.id)
    name = message.text
    storage.add('admin_post' + user_id, name)
    await bot.send_message(chat_id=message.chat.id, text="""Напиши текст поста""")


async def approve_post_message(message: Message, bot: AsyncTeleBot):
    user_id = str(message.from_user.id)
    name = storage.get('admin_post' + user_id)
    body = message.text
    storage.add('admin_post_name' + user_id, name)
    storage.add('admin_post_body' + user_id, body)
    msg = "Получился такой пост:\n" + f"{name}\n" + f"{body}\n\n"
    await bot.send_message(chat_id=message.chat.id, text=msg, reply_markup=keyboard.approve_post())


async def send_post(call: CallbackQuery, bot: AsyncTeleBot):
    user_id = call.from_user.id
    storage.delete('admin_post' + str(user_id))
    name = storage.get('admin_post_name' + str(user_id))
    body = storage.get('admin_post_body' + str(user_id))
    msg = body
    all_users = db.get_all_users()
    count = 0
    for user in all_users:
        if user["_id"] != user_id:
            try:
                print(user["chat_id"])
                await bot.send_message(chat_id=user["chat_id"], text=msg)
            except BaseException as e:
                continue
            else:
                count += 1
    post = Post(
        _id=None,
        name=name,
        body=body,
        count_users=count,
        user_id=user_id,
        date=datetime.now()
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


async def show_statistics(call: CallbackQuery, bot: AsyncTeleBot):
    pass


async def add_advertising_post():
    pass
