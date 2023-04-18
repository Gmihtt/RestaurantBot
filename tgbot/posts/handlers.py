from telebot.async_telebot import AsyncTeleBot

from tgbot.filters import check_callback_text, find_callback_text, check_state
from tgbot.posts import add_post
from tgbot.posts import show_posts
from tgbot.posts.states import PostStates


def post_handlers(bot: AsyncTeleBot):
    add_post_handlers(bot)
    show_post_handlers(bot)


def add_post_handlers(bot: AsyncTeleBot):
    bot.register_callback_query_handler(add_post.post_name_message,
                                        func=lambda c: check_callback_text(c, "add_post"),
                                        pass_bot=True)
    bot.register_message_handler(add_post.post_body_message,
                                 func=lambda c: check_state(c, PostStates.Name),
                                 pass_bot=True)
    bot.register_message_handler(add_post.add_post_body,
                                 func=lambda c: check_state(c, PostStates.Body),
                                 pass_bot=True)
    bot.register_callback_query_handler(add_post.post_file_message,
                                        func=lambda c: check_callback_text(c, "add_new_photo_post"),
                                        pass_bot=True)
    bot.register_message_handler(add_post.add_post_file,
                                 content_types=['photo', 'text'],
                                 func=lambda c: check_state(c, PostStates.Files),
                                 pass_bot=True)
    bot.register_callback_query_handler(add_post.approve_post_message,
                                        func=lambda c: check_callback_text(c, "finish_photo_post"),
                                        pass_bot=True)
    bot.register_callback_query_handler(add_post.send_post,
                                        func=lambda c: check_callback_text(c, "push_post"),
                                        pass_bot=True)


def show_post_handlers(bot: AsyncTeleBot):
    bot.register_callback_query_handler(show_posts.find_posts_message,
                                        func=lambda c: check_callback_text(c, "find_post"),
                                        pass_bot=True)
    bot.register_callback_query_handler(show_posts.send_post_info,
                                        func=lambda c: find_callback_text(c, "post_id"),
                                        pass_bot=True)