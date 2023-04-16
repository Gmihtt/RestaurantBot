from telebot.types import CallbackQuery, Message
from tgbot.utils import states


def check_callback_text(call: CallbackQuery, text: str):
    return call.data == text


def find_callback_text(call: CallbackQuery, text: str):
    return call.data.find(text) != -1


def check_state(message: Message, state: states.States):
    user_id = str(message.from_user.id)
    val = states.get_state(user_id)
    return val is not None and val == state
