from enum import Enum
from typing import TypedDict

from telebot.asyncio_handler_backends import State


class States(Enum):
    HELP = 0
    START = 1
    SHOW_PLACES = 2
    SHOW_PLACE = 3


class UserState(State):
    state: States = States.START
