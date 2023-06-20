from typing import TypedDict, Optional, List, Dict, Any

from strenum import StrEnum

from tgbot.common_types import File, convert_file_to_dict, convert_dict_to_file


class Coordinates(TypedDict):
    longitude: float
    latitude: float


class PlaceType(StrEnum):
    Restaurant = "restaurant"
    Bar = "bar"
    Cafe = "cafe"
    Lounge = "lounge"
    Bakery = "bakery"
    Coffee = "coffee_house"


class Restaurant(TypedDict):
    mid_price: Optional[int]
    business_lunch: Optional[bool]
    business_lunch_price: Optional[int]
    kitchens: List[str]
    features: List[str]
    rating: Optional[float]
    vegan: Optional[bool]


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
    place_types: List[PlaceType]
    place: Optional[Restaurant]
    yandex_id: Optional[str]


def convert_doc_to_place(d: Dict[str, Any]) -> Place:
    place: Place = {
        "_id": d['_id'],
        "name": d['name'],
        "city": d['city'],
        "address": d['address'],
        "coordinates": {
            "longitude": d['coordinates']['longitude'],
            "latitude": d['coordinates']['latitude'],
        },
        "files": list(map(convert_dict_to_file, d['files'])),
        "phone": d.get('phone'),
        "url": d.get('url'),
        "work_interval": d.get('work_interval'),
        "description": d.get('description'),
        "last_modify_id": d.get('last_modify_id'),
        "yandex_id": d.get('yandex_id'),
        "place_types": [],
        "place": None
    }
    if d.get('place_types') is not None:
        place_types = list(map(PlaceType, d['place_types']))
        place['place_types'] = place_types
        if d.get('place') is not None:
            restaurant = Restaurant(
                    mid_price=d['place'].get('mid_price'),
                    business_lunch=d['place'].get('business_lunch'),
                    business_lunch_price=d['place'].get('business_lunch_price'),
                    kitchens=d['place'].get('kitchens', []),
                    rating=d['place'].get('rating'),
                    vegan=d['place'].get('vegan'),
                    features=d['place'].get('features', []),
            )
            place['place'] = restaurant
        else:
            place['place'] = None
    else:
        place['place_types'] = []
        place['place'] = None
    return place


def convert_place_to_doc(p: Place) -> Dict[str, Any]:
    d = dict(p)
    d['_id'] = str(p['_id'])
    d['place_types'] = list(map(lambda p_t: p_t.value, p['place_types']))
    d['files'] = list(map(convert_file_to_dict, p['files']))
    return d
