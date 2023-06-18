import logging
from typing import List, Optional, Any, Dict

from bson import ObjectId
from pymongo import GEO2D

from tgbot import config
from tgbot.databases.mongo_db import Database
from tgbot.places import place
from tgbot.places.place import Coordinates
from tgbot.utils import values


class PlaceCollection(Database):
    def __init__(self):
        Database.__init__(self, config.places_collection)
        self.collection.create_index([("coordinates", GEO2D)])

    def find_close_place(
            self,
            coordinates: Coordinates,
            user_id: str,
            skip: int,
            limit: int = 5) -> List[place.Place]:
        q = {"coordinates": {"$nearSphere": coordinates}}

        filters = values.get_all_values_from_map('filters_map', user_id)
        if filters.get('vegan') is not None and filters.get('vegan') != "False":
            q['place.vegan'] = True
        if filters.get('business') is not None and filters.get('business') != "False":
            q['place.features'] = {"$in": ["Бизнес-ланч"]}
        if filters.get('hookah') is not None and filters.get('hookah') != "False":
            q['place.features'] = {"$in": ["Кальян-бар"]}

        kitchens = values.get_list('kitchens', user_id)
        if kitchens:
            q['place.kitchens'] = {"$in": kitchens}

        if filters.get('mid_price') is not None:
            q['place.mid_price'] = {"$gte": int(filters['mid_price'])}
        else:
            q['place.mid_price'] = {"$gte": 300}

        if filters.get('rating') is not None:
            q['place.rating'] = {"$gte": float(filters['rating'])}
        else:
            q['place.rating'] = {"$gte": 4.0}

        place_types = values.get_list('place_types', user_id)
        if place_types:
            q['place_types'] = {"$in": place_types}
        else:
            q['place_types'] = {"$in": ["restaurant", "cafe"]}

        res_q = self.collection.find(q, skip=skip, limit=limit, )
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

    def find_places_by_ids(self, list_ids: List[str]) -> List[place.Place]:
        ids = list(map(ObjectId, list_ids))
        vals = self.collection.find({"_id": {"$in": ids}})
        res = []
        for val in vals:
            res.append(place.convert_doc_to_place(dict(val)))
        return res

    def update_place(self, p: place.Place):
        logging.info("update: " + str(p))
        new_place = place.convert_place_to_doc(p)
        new_place.pop('_id')
        self.collection.update_one({"_id": ObjectId(p['_id'])}, {"$set": new_place})

    def get_places_count(self) -> int:
        return self.collection.count_documents({})


place_collection = PlaceCollection()
