from datetime import datetime
from typing import TypedDict, Optional, List, Dict, Any

from tgbot.common_types import File


class Post(TypedDict):
    _id: Optional[str]
    name: str
    body: str
    count_users: int
    user_id: int
    date: datetime
    files: List[File]


def convert_doc_to_post(d: Dict[str, Any]) -> Post:
    return Post(
        _id=d["_id"],
        name=d["name"],
        body=d["body"],
        count_users=d["count_users"],
        user_id=d["user_id"],
        date=d["date"],
        files=d.get("files")
    )


def convert_post_to_doc(p: Post) -> Dict[str, Any]:
    d = dict(p)
    d.pop('_id')
    d['files'] = list(map(lambda f: (f[0], f[1].value), p.get('files')))
    return d
