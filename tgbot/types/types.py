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


def pretty_show_restaurant(rest: Restaurant) -> str:
    return "скоро появится реализация"


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


def pretty_show_place(place: Place) -> str:
    name = "Название: " + place['name'] + '\n'
    city = "Город: " + place['city'] + '\n'
    place_str = ""
    if place['place_type'] == Restaurant:
        place_str = pretty_show_restaurant(place['place']) + '\n'
    address = "Адресс" + place['address'] + '\n'
    telephone = "Телефон" + place['telephone'] + '\n'
    url = "" if place['url'] is None else place['url'] + '\n'
    work_interval = "Время работы" + place['work_interval'] + '\n'
    description = "" if place['description'] is None else place['description'] + '\n'
    return (
        name +
        city +
        place_str +
        address +
        telephone +
        url +
        work_interval +
        description
    )
