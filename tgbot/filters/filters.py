from telebot.types import CallbackQuery


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