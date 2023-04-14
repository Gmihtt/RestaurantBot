from telebot.async_telebot import AsyncTeleBot

from tgbot.admin.admin import show_admin_menu
from tgbot.admin.manage import add_admin_message, add_user_to_admin
from tgbot.admin.places import place_example, place_info_parse, place_type_parse, place_restaurant_parse, \
    place_parse_file, place_description_msg, place_city_chose, place_approve, push_place, place_file_message, \
    send_search_message, search_by_coords_message, delete_place
from tgbot.admin.posts import post_name_message, post_body_message, approve_post_message, \
    send_post, find_posts_message, send_post_info, add_post_body, post_photo_message, add_post_photo
from tgbot.commands.commands import check_welcome, send_welcome_callback, show_places_base, show_cur, show_back, \
    show_next, show_place, send_help
from tgbot.filters.filters import check_callback_text, find_callback_text, check_state_is_wait, check_state


def welcome_handlers(bot: AsyncTeleBot):
    bot.register_message_handler(check_welcome,
                                 commands=['start', 'restart'],
                                 pass_bot=True)
    bot.register_callback_query_handler(send_welcome_callback,
                                        func=lambda c: check_callback_text(c, "just_user"),
                                        pass_bot=True)


def user_handlers(bot: AsyncTeleBot):
    bot.register_message_handler(show_places_base,
                                 content_types=['location'],
                                 pass_bot=True)
    bot.register_callback_query_handler(show_cur,
                                        func=lambda c: check_callback_text(c, "places_cur"),
                                        pass_bot=True)
    bot.register_callback_query_handler(show_back,
                                        func=lambda c: check_callback_text(c, "places_back"),
                                        pass_bot=True)
    bot.register_callback_query_handler(show_next,
                                        func=lambda c: check_callback_text(c, "places_next"),
                                        pass_bot=True)
    bot.register_callback_query_handler(show_place,
                                        func=lambda c: find_callback_text(c, "place_id"),
                                        pass_bot=True)


def admin_handlers(bot: AsyncTeleBot):
    bot.register_callback_query_handler(show_admin_menu,
                                        func=lambda c: check_callback_text(c, "admin_user"),
                                        pass_bot=True)
    admin_post_handlers(bot)
    admin_place_handlers(bot)


def admin_post_handlers(bot: AsyncTeleBot):
    bot.register_callback_query_handler(post_name_message,
                                        func=lambda c: check_callback_text(c, "add_post"),
                                        pass_bot=True)
    bot.register_message_handler(post_body_message,
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
    bot.register_callback_query_handler(find_posts_message,
                                        func=lambda c: check_callback_text(c, "find_post"),
                                        pass_bot=True)
    bot.register_callback_query_handler(send_post_info,
                                        func=lambda c: find_callback_text(c, "post_id"),
                                        pass_bot=True)


def admin_place_handlers(bot: AsyncTeleBot):
    bot.register_callback_query_handler(place_example,
                                        func=lambda c: check_callback_text(c, "add_place"),
                                        pass_bot=True)
    bot.register_message_handler(place_info_parse,
                                 func=lambda c: check_state_is_wait(c, 'admin_place_info'),
                                 pass_bot=True)
    bot.register_callback_query_handler(place_type_parse,
                                        func=lambda c: find_callback_text(c, "place_type"),
                                        pass_bot=True)
    bot.register_message_handler(place_restaurant_parse,
                                 func=lambda c: check_state_is_wait(c, 'admin_restaurant_info'),
                                 pass_bot=True)
    bot.register_callback_query_handler(place_file_message,
                                        func=lambda c: check_callback_text(c, "add_new_photo_place"),
                                        pass_bot=True)
    bot.register_message_handler(place_parse_file,
                                 content_types=['photo', 'video', 'document'],
                                 func=lambda c: check_state(c, 'admin_place_files_count'),
                                 pass_bot=True)
    bot.register_callback_query_handler(place_description_msg,
                                        func=lambda c: check_callback_text(c, "finish_photo_place"),
                                        pass_bot=True)
    bot.register_message_handler(place_city_chose,
                                 func=lambda c: check_state_is_wait(c, 'admin_place_description'),
                                 pass_bot=True)
    bot.register_callback_query_handler(place_approve,
                                        func=lambda c: find_callback_text(c, "city_id"),
                                        pass_bot=True)
    bot.register_callback_query_handler(push_place,
                                        func=lambda c: check_callback_text(c, "push_place"),
                                        pass_bot=True)
    bot.register_callback_query_handler(send_search_message,
                                        func=lambda c: check_callback_text(c, "find_place"),
                                        pass_bot=True)
    bot.register_callback_query_handler(search_by_coords_message,
                                        func=lambda c: check_callback_text(c, "search_by_coords"),
                                        pass_bot=True)
    bot.register_callback_query_handler(delete_place,
                                        func=lambda c: find_callback_text(c, "delete_place"),
                                        pass_bot=True)
    bot.register_callback_query_handler(add_admin_message,
                                        func=lambda c: check_callback_text(c, "add_admin"),
                                        pass_bot=True)
    bot.register_message_handler(add_user_to_admin,
                                 func=lambda c: check_state(c, 'admin_restaurant_info'),
                                 pass_bot=True)


def other_handlers(bot: AsyncTeleBot):
    bot.register_message_handler(send_help,
                                 commands=['help'],
                                 pass_bot=True)
    bot.register_message_handler(send_help, content_types=['photo', 'text', 'video', 'document'], pass_bot=True)
