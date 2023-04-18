from typing import List, Optional, Any, Dict

from bson import ObjectId
from pymongo import GEO2D

from tgbot import config
from tgbot.databases.mongo_db import Database
from tgbot.places import place
from tgbot.places.place import Coordinates


class PlaceCollection(Database):
    def __init__(self):
        Database.__init__(self, config.places_collection)
        self.collection.create_index([("coordinates", GEO2D)])

    def find_close_place(self, coordinates: Coordinates, skip: int, limit: int = 10) -> List[place.Place]:
        q = {"coordinates": {"$near": coordinates}}
        res_q = self.collection.find(q, skip=skip, limit=limit)
        res = []
        for doc in res_q:
            res.append(place.convert_doc_to_place(doc))
        return res

    def find_place_by_id(self, place_id: str) -> Optional[place.Place]:
        val = self.collection.find_one({"_id": ObjectId(place_id)})
        if val is None:
            return None
        else:
            return place.convert_doc_to_place(dict(val))

    def find_place(self, doc: Dict[str, Any]) -> Optional[place.Place]:
        if len(doc) < 2:
            return None
        else:
            val = self.collection.find_one(doc)
            if val is None:
                return None
            else:
                return place.convert_doc_to_place(dict(val))

    def update_place(self, p: place.Place):
        new_place = place.convert_place_to_doc(p)
        self.collection.update_one({"_id": ObjectId(p['_id'])}, new_place)

    def get_places_count(self) -> int:
        return self.collection.count_documents({})


place_collection = PlaceCollection()
