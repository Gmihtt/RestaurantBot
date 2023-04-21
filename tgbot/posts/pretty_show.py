from tgbot.posts.post import Post


def pretty_show_post(post: Post) -> str:
    id = "id поста: " + str(post["_id"]) + '\n'
    name = "название поста: " + post["name"] + '\n'
    count_users = "количество пользователей до которых пост дошел: " + str(post["count_users"]) + '\n'
    date = "создан: " + str(post["date"])
    return id + name + count_users + date
