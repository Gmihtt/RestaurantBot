from strenum import StrEnum
from typing import TypedDict, Optional, Dict, Any


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
