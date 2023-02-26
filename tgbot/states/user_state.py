from telebot.asyncio_handler_backends import State


class UserState(State):
    HELP = 0
    START = 1
    CHOSE_PLACE = 2
    SEARCH = 3
    ADD_PLACE = 4
    MARK = 5
    ADMIN = 6
    ADD_GROUP = 7
    FAVORITE = 8
    GROUP = 9
    SHOW_PLACE = 10
