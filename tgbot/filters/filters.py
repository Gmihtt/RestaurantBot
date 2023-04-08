from telebot.types import CallbackQuery, Message

from tgbot.utils.database import storage


def check_user(call: CallbackQuery):
    return call.data == "just_user"


def check_admin(call: CallbackQuery):
    return call.data == "admin_user"


def places_cur(call: CallbackQuery):
    return call.data == "places_cur"


def places_back(call: CallbackQuery):
    return call.data == "places_back"


def places_next(call: CallbackQuery):
    return call.data == "places_next"


def place_id(call: CallbackQuery):
    return call.data.find("place_id") != -1


def check_add_post(call: CallbackQuery):
    return call.data == "add_post"


def check_edit_post(call: CallbackQuery):
    return call.data == "edit_post"


def check_find_post(call: CallbackQuery):
    return call.data == "find_post"


def check_delete_post(call: CallbackQuery):
    return call.data == "delete_post"


def check_add_place(call: CallbackQuery):
    return call.data == "add_place"


def check_edit_place(call: CallbackQuery):
    return call.data == "edit_place"


def check_add_admin(call: CallbackQuery):
    return call.data == "add_admin"


def check_delete_admin(call: CallbackQuery):
    return call.data == "delete_admin"


def check_find_place(call: CallbackQuery):
    return call.data == "find_place"


def check_statistics(call: CallbackQuery):
    return call.data == "statistics"


def check_return_start(call: CallbackQuery):
    return call.data == "return_start"


def check_active_users(call: CallbackQuery):
    return call.data == "active_users"


def check_all_places(call: CallbackQuery):
    return call.data == "all_places"


def check_post_name(message: Message):
    user_id = str(message.from_user.id)
    name = storage.get('admin_post_name' + user_id)
    return name is not None and name == "wait"


def check_post_body(message: Message):
    user_id = str(message.from_user.id)
    body = storage.get('admin_post_body' + user_id)
    return body is not None and body == "wait"


def check_post_photos(message: Message):
    user_id = str(message.from_user.id)
    count = storage.get('admin_photo_count' + user_id)
    return count is not None


def check_push_post(call: CallbackQuery):
    return call.data == "push_post"


def post_id(call: CallbackQuery):
    return call.data.find("post_id") != -1


def add_new_photo(call: CallbackQuery):
    return call.data == "add_new_photo"


def finish_photo(call: CallbackQuery):
    return call.data == "finish_photo"
