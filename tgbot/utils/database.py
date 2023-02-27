from typing import List, Tuple
from pymongo import MongoClient, GEO2D
from tgbot.types.types import Place
from tgbot.config import mongo_database, places_collection
import logging


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
        return self.places.insert_one(place).inserted_id

    def add_places(self, places: List[Place]) -> List[str]:
        logging.info("add: " + str(places))
        return self.places.insert_many(places).inserted_ids

    def get_all_places(self) -> List[Place]:
        return list(self.places.find())

    def find_close_place(self, coordinates: Tuple[float, float], count: int) -> List[Place]:
        q = {"coordinates": {"$near": coordinates}}
        return list(self.places.find(q).limit(count))


db = Database()
