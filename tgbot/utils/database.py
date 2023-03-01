from typing import List, Tuple, Optional, TypedDict, Dict, Any

from bson import ObjectId
from pymongo import MongoClient, GEO2D
from tgbot.types.types import Place, PlaceType, Restaurant
from tgbot.config import mongo_database, places_collection
import logging
import redis


def convert_doc_to_place(d: Dict[str, Any]) -> Place:
    return Place(
        _id=d['_id'],
        name=d['name'],
        city=d['city'],
        place_type=PlaceType(d['place_type']),
        place=Restaurant(
            menu=d['place']['menu'],
            mid_price=d['place']['menu'],
            business_lunch=d['place']['business_lunch'],
            business_lunch_price=d['place']['business_lunch_price'],
            kitchen=d['place']['kitchen']
        ),
        address=d['address'],
        coordinates=d['coordinates'],
        photos=d['photos'],
        telephone=d['telephone'],
        url=d['url'],
        work_interval=d['work_interval'],
        description=d['description'],
        last_modify_id=d['last_modify_id'],
    )


def convert_place_to_doc(p: Place) -> Dict[str, Any]:
    d = dict(p)
    d.pop('_id')
    print(d)
    if d.get('place_type') is not None:
        d['place_type'] = int(d.get('place_type'))
    return d


class Storage:
    def __init__(self) -> None:
        self.r = redis.StrictRedis(host="localhost", port=6379, password="", decode_responses=True)

    def add(self, key: str, val: str) -> bool:
        return self.r.set(key, val)

    def get(self, key: str) -> Optional[str]:
        return self.r.get(key)


class Database:
    def __init__(self) -> None:
        logging.basicConfig(filename='db.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[mongo_database]  # init db
        self.places = self.db[places_collection]  # init places collections
        self.places.create_index([("coordinates", GEO2D)])

    def add_place(self, place: Place) -> str:
        logging.info("add: " + str(place))
        doc = convert_place_to_doc(place)
        return self.places.insert_one(doc).inserted_id

    def add_places(self, places: List[Place]) -> List[str]:
        logging.info("add: " + str(places))
        doc = list(map(convert_place_to_doc, places))
        return self.places.insert_many(doc).inserted_ids

    def get_all_places(self) -> List[Place]:
        return list(map(convert_doc_to_place, self.places.find()))

    def find_close_place(self, coordinates: Tuple[float, float], skip: int, limit: int) -> List[Place]:
        q = {"coordinates": {"$near": coordinates}}
        res_q = self.places.find(q, skip=skip, limit=limit)
        res = []
        for doc in res_q:
            res.append(convert_doc_to_place(doc))
        return res

    def find_place(self, place_id: str) -> Optional[Place]:
        val = dict(self.places.find_one({"_id": ObjectId(place_id)}))
        if val is None:
            return None
        else:
            return convert_doc_to_place(val)


db = Database()
storage = Storage()
