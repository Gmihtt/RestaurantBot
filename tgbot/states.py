from typing import Union, Optional

from tgbot.databases.redis_storage import storage
from tgbot.places.states import PlaceStates


States = Union[PlaceStates]


def set_state(state: States, user_id: str):
    key = 'state' + user_id
    if type(state) == PlaceStates:
        val = 'place' + state.value
        storage.add_val(key, val)


def get_state(user_id: str) -> States:
    key = 'state' + user_id
    val = storage.get_val(key)
    if val is None:
        raise Exception(f"user with {user_id} don't have state!!")
    if val.find("place") != -1:
        return PlaceStates[val[len("place"):]]
