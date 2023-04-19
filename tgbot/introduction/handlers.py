from telebot.async_telebot import AsyncTeleBot

from tgbot.filters import check_callback_text
from tgbot.introduction import intro


def intro_handlers(bot: AsyncTeleBot):
    bot.register_message_handler(intro.check_welcome,
                                 commands=['start', 'restart'],
                                 pass_bot=True)
    bot.register_callback_query_handler(intro.send_welcome_callback,
                                        func=lambda c: check_callback_text(c, "just_user"),
                                        pass_bot=True)
    bot.register_callback_query_handler(intro.show_admin_menu,
                                        func=lambda c: check_callback_text(c, "admin_user"),
                                        pass_bot=True)
    bot.register_message_handler(intro.send_help,
                                 commands=['help'],
                                 pass_bot=True)
