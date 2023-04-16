from datetime import datetime
from typing import TypedDict, Optional, List, Dict, Any


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