from typing import List

from pymongo import MongoClient
from tgbot.types.types import Place
import logging


class Database:
    def __init__(self) -> None:
        logging.basicConfig(filename='db.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.tgbot
        self.places = self.db.tgbot_collections

    def add_place(self, place: Place) -> str:
        logging.info("add: " + str(place))
        return self.places.insert_one(place)

    def add_places(self, places: List[Place]) -> List[str]:
        logging.info("add: " + str(places))
        return self.places.insert_many(places)


db = Database()