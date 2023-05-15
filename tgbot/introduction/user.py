from datetime import datetime
from typing import Dict, Any, TypedDict, Optional, List


class User(TypedDict):
    _id: Optional[str]
    user_tg_id: int
    city: str
    chat_id: int
    is_admin: bool
    favorites: List[str]
    username: Optional[str]
    last_activity: datetime


def convert_doc_to_user(d: Dict[str, Any]) -> User:
    return User(
        _id=d['_id'],
        user_tg_id=d['user_tg_id'],
        chat_id=d['chat_id'],
        is_admin=d['is_admin'],
        username=d['username'],
        city=d['city'],
        favorites=d['favorites'],
        last_activity=d['last_activity']
    )


def convert_user_to_doc(u: User) -> Dict[str, Any]:
    d = dict(u)
    d.pop('_id')
    d['last_activity'] = u['last_activity']
    return d
