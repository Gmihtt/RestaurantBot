from telebot.async_telebot import AsyncTeleBot

from tgbot.introduction.handlers import intro_handlers
from tgbot.places.handlers import place_handlers
from tgbot.posts.handlers import post_handlers


def handlers(bot: AsyncTeleBot):
    intro_handlers(bot)
    place_handlers(bot)
    post_handlers(bot)
