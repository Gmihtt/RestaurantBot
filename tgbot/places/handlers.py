from telebot.async_telebot import AsyncTeleBot

from tgbot.filters import check_callback_text, find_callback_text, check_state
from tgbot.places import add_place, delete_place, find_place
from tgbot.places.states import PlaceStates


def place_handlers(bot: AsyncTeleBot):
    add_place_handlers(bot)
    delete_place_handlers(bot)
    find_place_handlers(bot)


def add_place_handlers(bot: AsyncTeleBot):
    bot.register_callback_query_handler(add_place.place_example,
                                        func=lambda c: check_callback_text(c, "add_place"),
                                        pass_bot=True)
    bot.register_message_handler(add_place.place_info_parse,
                                 func=lambda c: check_state(c, PlaceStates.AddInfo),
                                 pass_bot=True)
    bot.register_callback_query_handler(add_place.place_type_parse,
                                        func=lambda c: find_callback_text(c, "place_type"),
                                        pass_bot=True)
    bot.register_message_handler(add_place.place_restaurant_parse,
                                 func=lambda c: check_state(c, PlaceStates.AddRestaurantInfo),
                                 pass_bot=True)
    bot.register_callback_query_handler(add_place.place_file_message,
                                        func=lambda c: check_callback_text(c, "add_new_file_place"),
                                        pass_bot=True)
    bot.register_message_handler(add_place.place_parse_file,
                                 content_types=['photo', 'video', 'document'],
                                 func=lambda c: check_state(c, PlaceStates.AddFiles),
                                 pass_bot=True)
    bot.register_callback_query_handler(add_place.place_description_msg,
                                        func=lambda c: check_callback_text(c, "finish_file_place"),
                                        pass_bot=True)
    bot.register_message_handler(add_place.place_city_chose,
                                 func=lambda c: check_state(c, PlaceStates.AddDescription),
                                 pass_bot=True)
    bot.register_callback_query_handler(add_place.place_approve,
                                        func=lambda c: find_callback_text(c, "city_id"),
                                        pass_bot=True)
    bot.register_callback_query_handler(add_place.push_place,
                                        func=lambda c: check_callback_text(c, "push_place"),
                                        pass_bot=True)


def delete_place_handlers(bot: AsyncTeleBot):
    bot.register_callback_query_handler(delete_place.send_search_message,
                                        func=lambda c: check_callback_text(c, "find_place"),
                                        pass_bot=True)
    bot.register_callback_query_handler(delete_place.search_by_coords_message,
                                        func=lambda c: check_callback_text(c, "search_by_coords"),
                                        pass_bot=True)
    bot.register_callback_query_handler(delete_place.delete_place,
                                        func=lambda c: find_callback_text(c, "delete_place"),
                                        pass_bot=True)


def find_place_handlers(bot: AsyncTeleBot):
    bot.register_message_handler(find_place.show_places_by_coordinates,
                                 content_types=['location'],
                                 pass_bot=True)
    bot.register_callback_query_handler(find_place.show_cur,
                                        func=lambda c: check_callback_text(c, "places_cur"),
                                        pass_bot=True)
    bot.register_callback_query_handler(find_place.show_back,
                                        func=lambda c: check_callback_text(c, "places_back"),
                                        pass_bot=True)
    bot.register_callback_query_handler(find_place.show_next,
                                        func=lambda c: check_callback_text(c, "places_next"),
                                        pass_bot=True)
    bot.register_callback_query_handler(find_place.show_place,
                                        func=lambda c: find_callback_text(c, "place_id"),
                                        pass_bot=True)
