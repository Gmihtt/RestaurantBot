from typing import Union

from tgbot.databases.redis_storage import storage
from tgbot.introduction.states import IntroStates
from tgbot.places.states import PlaceStates
from tgbot.posts.states import PostStates

States = Union[PlaceStates, IntroStates, PostStates]


def set_state(state: States, user_id: str):
    key = 'state' + user_id
    if type(state) == PlaceStates:
        val = 'place' + state
        storage.add_value(key, val)
    if type(state) == IntroStates:
        val = 'intro' + state
        storage.add_value(key, val)
    if type(state) == PostStates:
        val = 'post' + state
        storage.add_value(key, val)


def get_state(user_id: str) -> States:
    key = 'state' + user_id
    val = storage.get_value(key)

    if val is None:
        raise Exception(f"user with {user_id} don't have state!!")

    if val.find("place") != -1:
        return PlaceStates[val[len("place"):]]
    if val.find("intro") != -1:
        return IntroStates[val[len("intro"):]]
    if val.find("post") != -1:
        return PostStates[val[len("post"):]]
