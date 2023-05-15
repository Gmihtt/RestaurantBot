from typing import Union

from telebot.types import CallbackQuery, Message
from tgbot.utils import states


def check_callback_text(call: CallbackQuery, text: str):
    return call.data == text


def find_callback_text(call: CallbackQuery, text: str):
    return call.data.find(text) != -1


def check_state(obj: Union[Message, CallbackQuery], state: states.States):
    val = states.get_state(str(obj.from_user.id))
    return val is not None and val == state
