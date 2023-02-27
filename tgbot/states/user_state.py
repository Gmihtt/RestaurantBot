from telebot.asyncio_handler_backends import State


class UserState(State):
    HELP = 0
    START = 1
    CHOSE_PLACE = 2
