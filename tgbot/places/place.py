from enum import auto
from typing import TypedDict, Optional, Union, List, Dict, Any

from strenum import StrEnum

from tgbot.common_types import File


class Coordinates(TypedDict):
    first: float
    second: float


class PlaceType(StrEnum):
    Restaurant = auto()


class Restaurant(TypedDict):
    mid_price: Optional[int]
    business_lunch: bool
    business_lunch_price: Optional[int]
    kitchen: str
    vegan: bool


class Place(TypedDict):
    _id: Optional[str]
    name: str
    city: str
    address: str
    coordinates: Coordinates
    phone: Optional[str]
    url: Optional[str]
    work_interval: Optional[str]
    description: Optional[str]
    last_modify_id: Optional[int]
    files: List[File]
    place_type: Optional[PlaceType]
    place: Union[Restaurant, None]


def convert_doc_to_place(d: Dict[str, Any]) -> Place:
    place = {
        "_id": d['_id'],
        "name": d['name'],
        "city": d['city'],
        "address": d['address'],
        "coordinates": {
            "first": d['coordinates']['first'],
            "second": d['coordinates']['second'],
        },
        "files": d['files'],
        "phone": d.get('phone'),
        "url": d.get('url'),
        "work_interval": d.get('work_interval'),
        "description": d.get('description'),
        "last_modify_id": d.get('last_modify_id'),
    }
    if d.get('place_type') is not None:
        place_type = PlaceType(d['place_type'])
        place['place_type'] = place_type
        if place_type == PlaceType.Restaurant:
            restaurant = Restaurant(
                mid_price=d['place'].get('mid_price'),
                business_lunch=d['place']['business_lunch'],
                business_lunch_price=d['place'].get('business_lunch_price'),
                kitchen=d['place']['kitchen'],
                vegan=d['place']['vegan']
            )
            place['place'] = restaurant
    else:
        place['place_type'] = None
        place['place'] = None
    return place


def convert_place_to_doc(p: Place) -> Dict[str, Any]:
    d = dict(p)
    d['place_type'] = p.get('place_type').value
    d['files'] = list(map(lambda f: (f[0], f[1].value), p.get('files')))
    return d
