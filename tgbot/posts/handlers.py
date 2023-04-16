from telebot.async_telebot import AsyncTeleBot

from tgbot.filters import check_callback_text, find_callback_text, check_state
from tgbot.posts import add_post


def add_post_handlers(bot: AsyncTeleBot):
    bot.register_callback_query_handler(add_post.post_name_message,
                                        func=lambda c: check_callback_text(c, "add_post"),
                                        pass_bot=True)
    bot.register_message_handler(add_post.post_body_message,
                                 func=lambda c: check_state_is_wait(c, 'admin_post_name'),
                                 pass_bot=True)
    bot.register_message_handler(add_post_body,
                                 func=lambda c: check_state_is_wait(c, 'admin_post_body'),
                                 pass_bot=True)
    bot.register_callback_query_handler(post_photo_message,
                                        func=lambda c: check_callback_text(c, "add_new_photo_post"),
                                        pass_bot=True)
    bot.register_message_handler(add_post_photo,
                                 content_types=['photo', 'text'],
                                 func=lambda c: check_state(c, 'admin_photo_count'),
                                 pass_bot=True)
    bot.register_callback_query_handler(approve_post_message,
                                        func=lambda c: check_callback_text(c, "finish_photo_post"),
                                        pass_bot=True)
    bot.register_callback_query_handler(send_post,
                                        func=lambda c: check_callback_text(c, "push_post"),
                                        pass_bot=True)


def show_post_handlers(bot: AsyncTeleBot):
    bot.register_callback_query_handler(find_posts_message,
                                        func=lambda c: check_callback_text(c, "find_post"),
                                        pass_bot=True)
    bot.register_callback_query_handler(send_post_info,
                                        func=lambda c: find_callback_text(c, "post_id"),
                                        pass_bot=True)