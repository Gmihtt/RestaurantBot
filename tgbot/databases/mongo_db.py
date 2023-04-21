from pymongo import MongoClient
from tgbot import config


class Database:
    def __init__(self, collection_name: str) -> None:
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[config.mongo_database]  # init db
        self.collection = self.db[collection_name]