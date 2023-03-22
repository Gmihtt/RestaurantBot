from datetime import datetime
from enum import IntEnum
from typing import TypedDict, Tuple, Optional, Union, List, Dict, Any


class Admin(TypedDict):
    _id: Optional[str]
    user_id: str


def convert_doc_to_admin(d: Dict[str, Any]) -> Admin:
    return Admin(
        _id=d["_id"],
        user_id=d["user_id"]
    )


def convert_admin_to_doc(a: Admin) -> Dict[str, Any]:
    d = dict(a)
    d.pop('_id')
    return d


class User(TypedDict):
    _id: Optional[str]
    user_tg_id: int
    chat_id: int
    username: str


def convert_doc_to_user(d: Dict[str, Any]) -> User:
    return User(
        _id=d["_id"],
        user_tg_id=d["user_tg_id"],
        chat_id=d["chat_id"],
        username=d["username"],
    )


def convert_user_to_doc(u: User) -> Dict[str, Any]:
    d = dict(u)
    d.pop('_id')
    return d


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


def convert_doc_to_place(d: Dict[str, Any]) -> Place:
    return Place(
        _id=d['_id'],
        name=d['name'],
        city=d['city'],
        place_type=PlaceType(d['place_type']),
        place=Restaurant(
            menu=d['place']['menu'],
            mid_price=d['place']['menu'],
            business_lunch=d['place']['business_lunch'],
            business_lunch_price=d['place']['business_lunch_price'],
            kitchen=d['place']['kitchen']
        ),
        address=d['address'],
        coordinates=d['coordinates'],
        photos=d['photos'],
        telephone=d['telephone'],
        url=d['url'],
        work_interval=d['work_interval'],
        description=d['description'],
        last_modify_id=d['last_modify_id'],
    )


def convert_place_to_doc(p: Place) -> Dict[str, Any]:
    d = dict(p)
    d.pop('_id')
    if d.get('place_type') is not None:
        d['place_type'] = int(d.get('place_type'))
    return d


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


class Post(TypedDict):
    _id: Optional[str]
    name: str
    body: str
    count_users: int
    message_id: int
    user_id: int
    date: datetime


def convert_doc_to_post(d: Dict[str, Any]) -> Post:
    return Post(
        _id=d["_id"],
        name=d["name"],
        body=d["body"],
        count_users=d["count_users"],
        message_id=d["message_id"],
        user_id=d["user_id"],
        date=d["date"]
    )


def convert_post_to_doc(u: Post) -> Dict[str, Any]:
    d = dict(u)
    d.pop('_id')
    return d
