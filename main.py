import asyncio

import typing

from telebot.asyncio_filters import StateFilter

from tgbot.commands.commands import send_welcome, send_help, show_places_base, show_place, \
    show_cur, show_back, show_next, check_welcome
from tgbot.filters.filters import place_id, places_back, places_next, places_cur, check_user

# telebot
from telebot.async_telebot import AsyncTeleBot
# config
from tgbot import config
import logging

logging.basicConfig(filename='db.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
bot = AsyncTeleBot(config.TOKEN)


def register_handlers():
    bot.register_message_handler(check_welcome, commands=['start', 'restart'], pass_bot=True)
    bot.register_callback_query_handler(check_welcome, func=check_user, pass_bot=True)
    bot.register_message_handler(send_help, commands=['help'], pass_bot=True)
    bot.register_message_handler(show_places_base, content_types=['location'], pass_bot=True)
    bot.register_callback_query_handler(show_cur,
                                        func=places_cur,
                                        pass_bot=True)
    bot.register_callback_query_handler(show_back,
                                        func=places_back,
                                        pass_bot=True)
    bot.register_callback_query_handler(show_next,
                                        func=places_next,
                                        pass_bot=True)
    bot.register_callback_query_handler(show_place, func=place_id, pass_bot=True)
    bot.register_message_handler(send_help, content_types=['text'], pass_bot=True)


register_handlers()


async def run():
    await bot.polling(non_stop=True)


bot.add_custom_filter(StateFilter(bot))

asyncio.run(run())
