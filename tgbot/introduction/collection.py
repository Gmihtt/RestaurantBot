import logging
from datetime import datetime
from typing import Optional, List

from bson import ObjectId

from tgbot import config
from tgbot.databases.mongo_db import Database
from tgbot.introduction import user


class UserCollection(Database):
    def __init__(self):
        Database.__init__(self, config.users_collection)

    def add_user(self, u: user.User) -> str:
        logging.info("add user: " + str(u))
        if self.get_user_by_tg_id(u["user_tg_id"]) is None:
            val = user.convert_user_to_doc(u)
            return self.collection.insert_one(val).inserted_id

    def get_all_users(self) -> List[user.User]:
        users = self.collection.find({})
        res = []
        for u in users:
            res.append(user.convert_doc_to_user(u))
        return res

    def get_user_by_id(self, _id: str) -> Optional[user.User]:
        val = self.collection.find_one({"_id": ObjectId(_id)})
        if val is None:
            return None
        else:
            return user.convert_doc_to_user(dict(val))

    def get_user_by_tg_id(self, user_tg_id: int) -> Optional[user.User]:
        if type(user_tg_id) is str:
            user_tg_id = int(user_tg_id)
        val = self.collection.find_one({"user_tg_id": user_tg_id})
        if val is None:
            return None
        else:
            return user.convert_doc_to_user(dict(val))

    def get_user_by_username(self, username: str) -> Optional[user.User]:
        val = self.collection.find_one({"username": username})
        if val is None:
            return None
        else:
            return user.convert_doc_to_user(dict(val))

    def update_favorites(self, user_tg_id: int, new_favorites: List[str]):
        self.collection.update_one({"user_tg_id": user_tg_id}, {"$set": {"favorites": new_favorites}})

    def set_city(self, user_tg_id: int, city: str):
        return self.collection.update_one({"user_tg_id": user_tg_id}, {"$set": {"city": city}})

    def set_last_activity(self, user_tg_id: int):
        return self.collection.update_one({"user_tg_id": user_tg_id}, {"$set": {"last_activity": datetime.now()}})

    def add_admin(self, username: str) -> Optional[str]:
        return self.collection.update_one({"username": username}, {"$set": {"is_admin": True}})

    def delete_admin(self, username: str) -> bool:
        return self.collection.update_one({"username": username}, {"$set": {"is_admin": False}})

    def is_admin(self, user_id: int):
        u = self.collection.find_one({"user_tg_id": user_id})
        return u.get('is_admin')


user_collection = UserCollection()
