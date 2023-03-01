from enum import IntEnum
from typing import TypedDict, Tuple, Optional, Union, List


class User(TypedDict):
    admin: bool
    user_id: int
    user_name: Optional[str]
    chat_id: str


class PlaceType(IntEnum):
    RESTAURANT = 0


class Restaurant(TypedDict):
    menu: str  # file
    mid_price: Optional[int]
    business_lunch: bool
    business_lunch_price: Optional[int]
    kitchen: Optional[str]


class Place(TypedDict):
    _id: Optional[str]
    name: str
    city: str
    place_type: PlaceType
    place: Union[Restaurant]
    address: str
    coordinates: Tuple[float, float]
    photos: Optional[List[str]]
    telephone: str
    url: Optional[str]
    work_interval: str
    description: Optional[str]
    last_modify_id: int
