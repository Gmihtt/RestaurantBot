import logging
from datetime import datetime
from typing import Optional, List, Dict, Any

from bson import ObjectId

from tgbot import config
from tgbot.databases.mongo_db import Database
from tgbot.introduction import user


class StatisticsCollection(Database):
    def __init__(self):
        Database.__init__(self, config.statistics_collection)

    def new_user_deeplink(self, code: str, user_id: str) -> str:
        res = self.get_stat_by_code(code)
        if res is None:
            val = {
                'code': code,
                'user_ids': [user_id]
            }
            return self.collection.insert_one(val).inserted_id
        else:
            user_ids: List[str] = res['user_ids']
            user_ids.append(user_id)
            return self.collection.update_one({'code': code}, {"$set": {"user_ids": user_ids}}).upserted_id

    def get_stat_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        val = self.collection.find_one({"code": code})
        if val is None:
            return None
        else:
            res = dict(val)
            res.pop("_id")
            return res

    def get_all_codes(self):
        codes = self.collection.find({}, {'code': True, '_id': False})
        res = []
        for code in codes:
            res.append(code['code'])
        return res


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
        return list(map(user.convert_doc_to_user, users))

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
        return u.get('is_admin') is not None

    def users_stat(self, time: datetime, user_ids: Optional[List[str]] = None) -> int:
        if user_ids is None:
            v = {
                'last_activity': {"$gte": time},
            }
        else:
            ids: List[ObjectId] = list(map(ObjectId, user_ids))
            v = {
                'last_activity': {"$gte": time},
                '_id': {"$in": ids}
            }
        users = self.collection.find(v)

        return len(list(users))

    def users_count(self):
        return self.collection.count_documents({})


user_collection = UserCollection()
stat_collection = StatisticsCollection()
