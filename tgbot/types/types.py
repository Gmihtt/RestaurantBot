from datetime import datetime
from enum import Enum
from strenum import StrEnum
from typing import TypedDict, Tuple, Optional, Union, List, Dict, Any


class FileTypes(StrEnum):
    Photo = "photo"
    Video = "video"
    Document = "document"


class File(TypedDict):
    file_id: str
    file: FileTypes


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


class PlaceType(Enum):
    RESTAURANT = "RESTAURANT"


class Restaurant(TypedDict):
    mid_price: Optional[int]
    business_lunch: bool
    business_lunch_price: Optional[int]
    kitchen: Optional[str]


class Place(TypedDict):
    _id: Optional[str]
    name: str
    city: str  # city_id
    place_type: PlaceType
    place: Union[Restaurant]
    address: str
    coordinates: Tuple[float, float]
    files: List[File]
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
        place_type=PlaceType(d['place_type'].upper()),
        place=Restaurant(
            mid_price=d['place']['mid_price'],
            business_lunch=d['place']['business_lunch'],
            business_lunch_price=d['place']['business_lunch_price'],
            kitchen=d['place']['kitchen']
        ),
        address=d['address'],
        coordinates=d['coordinates'],
        files=d['files'],
        telephone=d['telephone'],
        url=d['url'],
        work_interval=d['work_interval'],
        description=d['description'],
        last_modify_id=d['last_modify_id'],
    )


def convert_place_to_doc(p: Place) -> Dict[str, Any]:
    d = dict(p)
    d.pop('_id')
    d['place_type'] = p.get('place_type').value
    d['files'] = list(map(lambda f: (f[0], f[1].value), p.get('files')))
    return d


class Post(TypedDict):
    _id: Optional[str]
    name: str
    body: str
    count_users: int
    user_id: int
    date: datetime
    photos: List[str]


def convert_doc_to_post(d: Dict[str, Any]) -> Post:
    return Post(
        _id=d["_id"],
        name=d["name"],
        body=d["body"],
        count_users=d["count_users"],
        user_id=d["user_id"],
        date=d["date"],
        photos=d.get("photos")
    )


def convert_post_to_doc(u: Post) -> Dict[str, Any]:
    d = dict(u)
    d.pop('_id')
    return d


def pretty_show_post(post: Post) -> str:
    id = "id поста: " + str(post["_id"]) + '\n'
    name = "название поста: " + post["name"] + '\n'
    count_users = "количество пользователей до которых пост дошел: " + str(post["count_users"]) + '\n'
    date = "создан: " + str(post["date"])
    return id + name + count_users + date


class City(TypedDict):
    _id: Optional[str]
    name: str
    city_id: str


def convert_doc_to_city(d: Dict[str, Any]) -> City:
    return City(
        _id=d["_id"],
        name=d["name"],
        city_id=d["city_id"]
    )
