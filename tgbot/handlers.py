from telebot.async_telebot import AsyncTeleBot

from tgbot.admin.posts import post_name_message, post_body_message, approve_post_message, \
    send_post, find_posts_message, send_post_info, add_post_body, post_photo_message, add_post_photo
from tgbot.filters import check_callback_text, find_callback_text, check_state
from tgbot.introduction.handlers import intro_handlers
from tgbot.places.handlers import place_handlers


def handlers(bot: AsyncTeleBot):
    place_handlers(bot)
    intro_handlers(bot)

