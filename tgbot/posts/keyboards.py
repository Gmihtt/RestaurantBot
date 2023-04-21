from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def show_post():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Редактировать пост', callback_data="edit_post"),
               InlineKeyboardButton('Удалить пост', callback_data="delete_post"),
               InlineKeyboardButton('Вернуться в меню', callback_data="admin_user"),
               row_width=1)


def show_statistics():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Количество активных юзеров', callback_data="active_users"),
               InlineKeyboardButton('Количество юзеров за все время', callback_data="all_users"),
               InlineKeyboardButton('Количество мест', callback_data="all_places"),
               row_width=1)
    return markup


def approve_post():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Выкатить пост', callback_data="push_post"),
               InlineKeyboardButton('Редактировать', callback_data="add_post"),
               row_width=2)
    markup.add(InlineKeyboardButton('Вернуться в меню', callback_data="admin_user"),
               row_width=1)
    return markup


def chose_post_find_option(posts):
    markup = InlineKeyboardMarkup()
    line = []
    for post in posts:
        line.append(InlineKeyboardButton(post['name'], callback_data="post_id" + str(post["_id"])))
        if len(line) == 2:
            markup.add(*line, row_width=2)
            line = []
    markup.add(InlineKeyboardButton('Вернуться в меню', callback_data="admin_user"),
               row_width=1)
    return markup

