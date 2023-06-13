from telebot.async_telebot import AsyncTeleBot

from tgbot.filters import check_callback_text, check_state
from tgbot.introduction import intro, statistics
from tgbot.introduction import filters
from tgbot.introduction.states import IntroStates


def intro_handlers(bot: AsyncTeleBot):
    menu_handlers(bot)
    filters_handlers(bot)


def menu_handlers(bot: AsyncTeleBot):
    bot.register_message_handler(intro.check_welcome,
                                 commands=['start', 'restart'],
                                 pass_bot=True)
    bot.register_callback_query_handler(intro.send_welcome_callback,
                                        func=lambda c: check_callback_text(c, "just_user"),
                                        pass_bot=True)
    bot.register_callback_query_handler(intro.send_welcome_callback,
                                        func=lambda c: check_callback_text(c, "main_menu"),
                                        pass_bot=True)
    bot.register_callback_query_handler(intro.show_admin_menu,
                                        func=lambda c: check_callback_text(c, "admin_user"),
                                        pass_bot=True)
    bot.register_callback_query_handler(intro.place_preview,
                                        func=lambda c: check_callback_text(c, "find_place"),
                                        pass_bot=True)
    bot.register_callback_query_handler(statistics.show_statistics,
                                        func=lambda c: check_callback_text(c, "statistics"),
                                        pass_bot=True)
    bot.register_callback_query_handler(statistics.deeplink,
                                        func=lambda c: check_callback_text(c, "deeplink"),
                                        pass_bot=True)
    bot.register_callback_query_handler(statistics.show_stat_by_cities,
                                        func=lambda c: check_callback_text(c, "cities"),
                                        pass_bot=True)
    bot.register_callback_query_handler(statistics.show_stat,
                                        func=lambda c: check_state(c, IntroStates.Statistics),
                                        pass_bot=True)
    bot.register_callback_query_handler(statistics.deeplink,
                                        func=lambda c: check_state(c, IntroStates.DeepLink),
                                        pass_bot=True
                                        )
    bot.register_callback_query_handler(statistics.show_stat_by_cities,
                                        func=lambda c: check_state(c, IntroStates.Cities),
                                        pass_bot=True
                                        )


def filters_handlers(bot: AsyncTeleBot):
    bot.register_callback_query_handler(filters.set_filters,
                                        func=lambda c: check_callback_text(c, "filters"),
                                        pass_bot=True)
    bot.register_callback_query_handler(filters.filter_kitchens,
                                        func=lambda c: check_callback_text(c, "chose_kitchens"),
                                        pass_bot=True)
    bot.register_callback_query_handler(filters.filter_kitchens,
                                        func=lambda c: check_state(c, IntroStates.Kitchens),
                                        pass_bot=True)
    bot.register_callback_query_handler(filters.filter_mid_price,
                                        func=lambda c: check_callback_text(c, "mid_price"),
                                        pass_bot=True)
    bot.register_callback_query_handler(filters.filter_mid_price,
                                        func=lambda c: check_state(c, IntroStates.MidPrice),
                                        pass_bot=True)
    bot.register_callback_query_handler(filters.filter_rating,
                                        func=lambda c: check_callback_text(c, "rating"),
                                        pass_bot=True)
    bot.register_callback_query_handler(filters.filter_rating,
                                        func=lambda c: check_state(c, IntroStates.Rating),
                                        pass_bot=True)
    bot.register_callback_query_handler(filters.filter_place_type,
                                        func=lambda c: check_callback_text(c, "place_types"),
                                        pass_bot=True)
    bot.register_callback_query_handler(filters.filter_place_type,
                                        func=lambda c: check_state(c, IntroStates.PlaceTypes),
                                        pass_bot=True)
    bot.register_callback_query_handler(filters.set_vegan,
                                        func=lambda c: check_callback_text(c, "vegan"),
                                        pass_bot=True)
    bot.register_callback_query_handler(filters.set_business,
                                        func=lambda c: check_callback_text(c, "business"),
                                        pass_bot=True)
    bot.register_callback_query_handler(filters.set_hookah,
                                        func=lambda c: check_callback_text(c, "hookah"),
                                        pass_bot=True)
    bot.register_callback_query_handler(filters.msg_drop_filters,
                                        func=lambda c: check_callback_text(c, "filters_drop"),
                                        pass_bot=True)
    bot.register_callback_query_handler(filters.drop_filters,
                                        func=lambda c: check_callback_text(c, "drop_yes"),
                                        pass_bot=True)
    bot.register_callback_query_handler(filters.return_from_drop,
                                        func=lambda c: check_callback_text(c, "drop_no"),
                                        pass_bot=True)
