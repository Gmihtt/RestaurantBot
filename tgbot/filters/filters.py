from telebot.types import CallbackQuery, Message

from tgbot.databases.database import storage


def check_callback_text(call: CallbackQuery, text: str):
    return call.data == text


def find_callback_text(call: CallbackQuery, text: str):
    return call.data.find(text) != -1


def check_state_is_wait(message: Message, state: str):
    user_id = str(message.from_user.id)
    val = storage.get(state + user_id)
    return val is not None and val == "wait"


def check_state(message: Message, state: str):
    user_id = str(message.from_user.id)
    val = storage.get(state + user_id)
    return val is not None
