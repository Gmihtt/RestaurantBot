from telebot.async_telebot import AsyncTeleBot

from tgbot.filters import check_callback_text, find_callback_text, check_state
from tgbot.places import edit_place, find_place
from tgbot.places.states import PlaceStates


def place_handlers(bot: AsyncTeleBot):
    # edit_place_handlers(bot)
    find_place_handlers(bot)


"""
def edit_place_handlers(bot: AsyncTeleBot):
    bot.register_callback_query_handler(edit_place.place_search_message,
                                        func=lambda c: check_callback_text(c, "place"),
                                        pass_bot=True)
    bot.register_message_handler(edit_place.place_search_parse,
                                 func=lambda c: check_state(c, PlaceStates.Search),
                                 pass_bot=True)
    bot.register_message_handler(edit_place.place_restaurant_parse,
                                 func=lambda c: check_state(c, PlaceStates.AddRestaurantInfo),
                                 pass_bot=True)
    bot.register_callback_query_handler(edit_place.add_kitchen,
                                        func=lambda c: check_state(c, PlaceStates.AddRestaurantInfo),
                                        pass_bot=True)
    bot.register_callback_query_handler(edit_place.place_file_message,
                                        func=lambda c: check_callback_text(c, "add_new_file_place"),
                                        pass_bot=True)
    bot.register_message_handler(edit_place.place_parse_file,
                                 content_types=['photo', 'video', 'document'],
                                 func=lambda c: check_state(c, PlaceStates.AddFiles),
                                 pass_bot=True)
    bot.register_callback_query_handler(edit_place.place_description_msg,
                                        func=lambda c: check_callback_text(c, "finish_file_place"),
                                        pass_bot=True)
    bot.register_message_handler(edit_place.place_approve,
                                 func=lambda c: check_state(c, PlaceStates.AddDescription),
                                 pass_bot=True)
    bot.register_callback_query_handler(edit_place.push_place,
                                        func=lambda c: check_callback_text(c, "push_place"),
                                        pass_bot=True)
"""


def find_place_handlers(bot: AsyncTeleBot):
    bot.register_message_handler(find_place.show_places_by_coordinates,
                                 content_types=['location'],
                                 pass_bot=True)
    bot.register_callback_query_handler(find_place.show_cur,
                                        func=lambda c: check_callback_text(c, "places_cur"),
                                        pass_bot=True)
    bot.register_callback_query_handler(find_place.show_drop_filters,
                                        func=lambda c: check_callback_text(c, "without_filters"),
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
    bot.register_callback_query_handler(find_place.send_location,
                                        func=lambda c: find_callback_text(c, "place_position"),
                                        pass_bot=True)
    bot.register_callback_query_handler(find_place.send_phone,
                                        func=lambda c: find_callback_text(c, "place_phone"),
                                        pass_bot=True)
    bot.register_callback_query_handler(find_place.send_site,
                                        func=lambda c: find_callback_text(c, "place_site"),
                                        pass_bot=True)
    bot.register_callback_query_handler(find_place.show_favorite_places,
                                        func=
                                        lambda c: find_callback_text(c, "favorites"),
                                        pass_bot=True)
    bot.register_callback_query_handler(find_place.show_favorite_places,
                                        func=lambda c: check_state(c, PlaceStates.FavoritePlaces),
                                        pass_bot=True)
    bot.register_callback_query_handler(find_place.favorite_change,
                                        func=lambda c: find_callback_text(c, "favorite_delete"),
                                        pass_bot=True)
    bot.register_callback_query_handler(find_place.favorite_change,
                                        func=lambda c: find_callback_text(c, "favorite_add"),
                                        pass_bot=True)
    bot.register_callback_query_handler(find_place.favorite_change,
                                        func=lambda c: check_state(c, PlaceStates.FavoriteDelete),
                                        pass_bot=True)
