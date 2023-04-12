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
from tgbot.filters.filters import check_user, check_admin, check_add_post, check_post_name, check_post_body, \
    check_push_post, check_find_post, post_id, places_cur, places_back, places_next, place_id, add_new_photo_post, \
    check_post_photos, finish_photo_post, place_info, check_add_place, place_type, place_restaurant, finish_photo_place, \
    add_description, city_chose, add_new_photo_place, check_place_files, check_place_approve, check_find_place, \
    check_search_by_coords, delete_place_check, check_add_admin, wait_add_admin


def welcome_handlers(bot: AsyncTeleBot):
    bot.register_message_handler(check_welcome,
                                 commands=['start', 'restart'],
                                 pass_bot=True)
    bot.register_callback_query_handler(send_welcome_callback,
                                        func=check_user,
                                        pass_bot=True)


def user_handlers(bot: AsyncTeleBot):
    bot.register_message_handler(show_places_base,
                                 content_types=['location'],
                                 pass_bot=True)
    bot.register_callback_query_handler(show_cur,
                                        func=places_cur,
                                        pass_bot=True)
    bot.register_callback_query_handler(show_back,
                                        func=places_back,
                                        pass_bot=True)
    bot.register_callback_query_handler(show_next,
                                        func=places_next,
                                        pass_bot=True)
    bot.register_callback_query_handler(show_place,
                                        func=place_id,
                                        pass_bot=True)


def admin_handlers(bot: AsyncTeleBot):
    bot.register_callback_query_handler(show_admin_menu,
                                        func=check_admin,
                                        pass_bot=True)
    admin_post_handlers(bot)
    admin_place_handlers(bot)


def admin_post_handlers(bot: AsyncTeleBot):
    bot.register_callback_query_handler(post_name_message,
                                        func=check_add_post,
                                        pass_bot=True)
    bot.register_message_handler(post_body_message,
                                 func=check_post_name,
                                 pass_bot=True)
    bot.register_message_handler(add_post_body,
                                 func=check_post_body,
                                 pass_bot=True)
    bot.register_callback_query_handler(post_photo_message,
                                        func=add_new_photo_post,
                                        pass_bot=True)
    bot.register_message_handler(add_post_photo,
                                 content_types=['photo', 'text'],
                                 func=check_post_photos,
                                 pass_bot=True)
    bot.register_callback_query_handler(approve_post_message,
                                        func=finish_photo_post,
                                        pass_bot=True)
    bot.register_callback_query_handler(send_post,
                                        func=check_push_post,
                                        pass_bot=True)
    bot.register_callback_query_handler(find_posts_message,
                                        func=check_find_post,
                                        pass_bot=True)
    bot.register_callback_query_handler(send_post_info,
                                        func=post_id,
                                        pass_bot=True)


def admin_place_handlers(bot: AsyncTeleBot):
    bot.register_callback_query_handler(place_example,
                                        func=check_add_place,
                                        pass_bot=True)
    bot.register_message_handler(place_info_parse,
                                 func=place_info,
                                 pass_bot=True)
    bot.register_callback_query_handler(place_type_parse,
                                        func=place_type,
                                        pass_bot=True)
    bot.register_message_handler(place_restaurant_parse,
                                 func=place_restaurant,
                                 pass_bot=True)
    bot.register_callback_query_handler(place_file_message,
                                        func=add_new_photo_place,
                                        pass_bot=True)
    bot.register_message_handler(place_parse_file,
                                 content_types=['photo', 'video', 'document'],
                                 func=check_place_files,
                                 pass_bot=True)
    bot.register_callback_query_handler(place_description_msg,
                                        func=finish_photo_place,
                                        pass_bot=True)
    bot.register_message_handler(place_city_chose,
                                 func=add_description,
                                 pass_bot=True)
    bot.register_callback_query_handler(place_approve,
                                        func=city_chose,
                                        pass_bot=True)
    bot.register_callback_query_handler(push_place,
                                        func=check_place_approve,
                                        pass_bot=True)
    bot.register_callback_query_handler(send_search_message,
                                        func=check_find_place,
                                        pass_bot=True)
    bot.register_callback_query_handler(search_by_coords_message,
                                        func=check_search_by_coords,
                                        pass_bot=True)
    bot.register_callback_query_handler(delete_place,
                                        func=delete_place_check,
                                        pass_bot=True)
    bot.register_callback_query_handler(add_admin_message,
                                        func=check_add_admin,
                                        pass_bot=True)
    bot.register_message_handler(add_user_to_admin,
                                 func=wait_add_admin,
                                 pass_bot=True)


def other_handlers(bot: AsyncTeleBot):
    bot.register_message_handler(send_help,
                                 commands=['help'],
                                 pass_bot=True)
    bot.register_message_handler(send_help, content_types=['photo', 'text', 'video', 'document'], pass_bot=True)
