from enum import auto
from typing import TypedDict, Tuple, Optional, Union, List, Dict, Any

from strenum import StrEnum

from tgbot.common_types import File


class PlaceType(StrEnum):
    Restaurant = auto()


class Restaurant(TypedDict):
    mid_price: Optional[int]
    business_lunch: bool
    business_lunch_price: Optional[int]
    kitchen: Optional[str]
    vegan: bool


class Place(TypedDict):
    _id: Optional[str]
    name: str
    city_id: str
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
        city_id=d['city_id'],
        place_type=PlaceType[d['place_type']],
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
