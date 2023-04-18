from typing import List, Tuple, Optional

import pymongo
from bson import ObjectId
from pymongo import MongoClient

from tgbot import common_types
from tgbot.places import place
from tgbot import config
import logging

from tgbot.posts import post


class DatabaseOld:
    def __init__(self) -> None:
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[config.mongo_database]  # init db
        self.users = self.db[config.users_collection]
        self.admins = self.db[config.admins_collection]
        self.posts = self.db[config.posts_collection]

    def add_user(self, user: common_types.User) -> str:
        logging.info("add user: " + str(user))
        if self.get_user_by_tg_id(user["user_tg_id"]) is None:
            val = common_types.convert_user_to_doc(user)
            return self.users.insert_one(val).inserted_id

    def get_all_users(self) -> [common_types.User]:
        users = self.users.find({})
        res = []
        for user in users:
            res.append(common_types.convert_doc_to_user(user))
        return res

    def get_user_by_id(self, _id: str) -> Optional[common_types.User]:
        val = self.users.find_one({"_id": ObjectId(_id)})
        if val is None:
            return None
        else:
            return common_types.convert_doc_to_user(dict(val))

    def get_user_by_tg_id(self, user_tg_id: int) -> Optional[common_types.User]:
        val = self.users.find_one({"user_tg_id": user_tg_id})
        if val is None:
            return None
        else:
            return common_types.convert_doc_to_user(dict(val))

    def get_user_by_username(self, username: str) -> Optional[common_types.User]:
        val = self.users.find_one({"username": username})
        if val is None:
            return None
        else:
            return common_types.convert_doc_to_user(dict(val))

    def add_admin(self, username: str) -> Optional[str]:
        user = self.get_user_by_username(username)
        if user is None:
            return None
        else:
            admin = common_types.Admin(_id=None, user_id=user["_id"])
            logging.info("add admin: " + str(user))
            val = common_types.convert_admin_to_doc(admin)
            return self.admins.insert_one(val).inserted_id

    def find_admin(self, _id: str) -> Optional[common_types.Admin]:
        val = self.admins.find_one({"_id": ObjectId(_id)})
        if val is None:
            return None
        else:
            return common_types.convert_doc_to_admin(dict(val))

    def delete_admin(self, username: str) -> bool:
        user = self.get_user_by_username(username)
        logging.info("delete admin: " + str(user))
        if user is None:
            return False
        else:
            _id = user["_id"]
            val = self.find_admin(_id)
            if self.find_admin(_id) is None:
                return False
            else:
                self.admins.delete_one({"_id": val["_id"]})
                return True

    def is_admin(self, user_id: int):
        user = self.get_user_by_tg_id(user_id)
        print(user)
        if user is None:
            return False
        else:
            return self.find_admin(user["_id"]) is not None

    def add_post(self, p: post.Post) -> str:
        logging.info("add post: " + str(p))
        val = post.convert_post_to_doc(p)
        return self.posts.insert_one(val).inserted_id

    def find_post_by_name(self, post_name) -> Optional[post.Post]:
        val = self.posts.find_one({"name": post_name})
        if val is None:
            return None
        else:
            return post.convert_doc_to_post(dict(val))

    def find_post_by_id(self, post_id: str) -> Optional[post.Post]:
        val = self.posts.find_one({"_id": ObjectId(post_id)})
        print(val)
        if val is None:
            return None
        else:
            print(val)
            return post.convert_doc_to_post(dict(val))

    def update_post(self, p: post.Post):
        val = post.convert_post_to_doc(p)
        return self.posts.update_one({"_id": ObjectId(p["_id"])}, val)

    def delete_post(self, p: post.Post):
        return self.posts.delete_one({"_id": ObjectId(p["_id"])})

    def get_posts(self) -> [post.Post]:
        posts = self.posts.find({}).limit(11).sort('date', pymongo.DESCENDING)
        res = []
        for p in posts:
            res.append(post.convert_doc_to_post(p))
        return res


class Database:
    def __init__(self, collection_name: str) -> None:
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[config.mongo_database]  # init db
        self.collection = self.db[collection_name]


db = DatabaseOld()
