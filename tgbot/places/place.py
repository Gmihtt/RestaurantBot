from typing import TypedDict, Optional, Union, List, Dict, Any

from strenum import StrEnum

from tgbot.common_types import File, convert_file_to_dict, convert_dict_to_file


class Coordinates(TypedDict):
    first: float
    second: float


class PlaceType(StrEnum):
    Restaurant = "restaurant"


class Restaurant(TypedDict):
    mid_price: Optional[int]
    business_lunch: bool
    business_lunch_price: Optional[int]
    kitchen: str
    vegan: bool


class Place(TypedDict):
    _id: str
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
        "files": list(map(convert_dict_to_file, d['files'])),
        "phone": d.get('phone'),
        "url": d.get('url'),
        "work_interval": d.get('work_interval'),
        "description": d.get('description'),
        "last_modify_id": d.get('last_modify_id'),
    }
    if d.get('place_type') is not None:
        place_type = PlaceType(d['place_type'])
        place['place_type'] = place_type
        if d.get('place') is not None:
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
            place['place'] = None
    else:
        place['place_type'] = None
        place['place'] = None
    return place


def convert_place_to_doc(p: Place) -> Dict[str, Any]:
    d = dict(p)
    print(d)
    d['_id'] = str(p['_id'])
    print(d['_id'])
    d['place_type'] = p.get('place_type').value
    print(d['place_type'])
    d['files'] = list(map(convert_file_to_dict, p['files']))
    print(d['files'])
    return d
