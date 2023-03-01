from tgbot.types.types import Place, Restaurant, PlaceType
from tgbot.utils.database import db, convert_place_to_doc


def filter_place_prefix(call: str):
    return call.find("place_id") != -1


def generate_places(count: int):
    for i in range(count):
        place = Place(
            _id=None,
            name="name" + str(i),
            city="city" + str(i),
            place_type=PlaceType.RESTAURANT,
            place=Restaurant(
                menu="",
                mid_price=None,
                business_lunch=False,
                business_lunch_price=None,
                kitchen=None
            ),
            address="address" + str(i),
            coordinates=(i, i),
            photos=None,
            telephone=str(i),
            url=None,
            work_interval="",
            description=None,
            last_modify_id=0,
        )
        db.add_place(place)

