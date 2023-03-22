from typing import List, Tuple, Optional, TypedDict, Dict, Any

import boto3
from bson import ObjectId
from pymongo import MongoClient, GEO2D

from tgbot import config
from tgbot.types.types import Place, User, convert_place_to_doc, convert_doc_to_place, \
    convert_user_to_doc, convert_doc_to_user, Admin, convert_admin_to_doc, convert_doc_to_admin, Post, \
    convert_post_to_doc, convert_doc_to_post
from tgbot.config import mongo_database, places_collection, users_collection, admins_collection, posts_collection
import logging
import redis


class Storage:
    def __init__(self) -> None:
        self.r = redis.StrictRedis(host="localhost", port=6379, password="", decode_responses=True)

    def add(self, key: str, val: str) -> bool:
        return self.r.set(key, val)

    def get(self, key: str) -> Optional[str]:
        return self.r.get(key)


class Database:
    def __init__(self) -> None:
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[mongo_database]  # init db
        self.places = self.db[places_collection]  # init places collections
        self.places.create_index([("coordinates", GEO2D)])
        self.users = self.db[users_collection]
        self.admins = self.db[admins_collection]
        self.posts = self.db[posts_collection]

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

    def find_close_place(self, coordinates: Tuple[float, float], skip: int, limit: int = 10) -> List[Place]:
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

    def get_places_count(self) -> int:
        return self.places.count_documents({})

    def add_user(self, user: User) -> str:
        logging.info("add user: " + str(user))
        val = convert_user_to_doc(user)
        return self.users.insert_one(val).inserted_id

    def get_users(self) -> [User]:
        users = self.users.find({})
        res = []
        for user in users:
            res.append(convert_doc_to_user(user))
        return res

    def get_user_by_id(self, _id: str) -> Optional[User]:
        val = dict(self.users.find_one({"_id": _id}))
        if val is None:
            return None
        else:
            return convert_doc_to_user(val)

    def get_user_by_tg_id(self, user_tg_id: int) -> Optional[User]:
        val = dict(self.users.find_one({"user_tg_id": user_tg_id}))
        if val is None:
            return None
        else:
            return convert_doc_to_user(val)

    def get_user_by_username(self, username: str) -> Optional[User]:
        val = dict(self.users.find_one({"username": username}))
        if val is None:
            return None
        else:
            return convert_doc_to_user(val)

    def add_admin(self, username: str) -> Optional[str]:
        user = self.get_user_by_username(username)
        if user is None:
            return None
        else:
            admin = Admin(_id=None, user_id=user["_id"])
            logging.info("add admin: " + str(user))
            val = convert_admin_to_doc(admin)
            return self.admins.insert_one(val).inserted_id

    def find_admin(self, _id: str) -> Optional[Admin]:
        val = dict(self.admins.find_one({"_id": _id}))
        if val is None:
            return None
        else:
            return convert_doc_to_admin(val)

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
                self.admins.delete_one({"_id": val._id})
                return True

    def is_admin(self, user_id: int):
        user = self.get_user_by_tg_id(user_id)
        if user is None:
            return False
        else:
            return self.find_admin(user["_id"]) is not None

    def add_post(self, post: Post) -> str:
        logging.info("add post: " + str(post))
        val = convert_post_to_doc(post)
        return self.posts.insert_one(val).inserted_id

    def find_post_by_name(self, post: Post) -> Optional[Post]:
        val = dict(self.posts.find_one({"name": post.name}))
        if val is None:
            return None
        else:
            return convert_doc_to_post(val)

    def find_post_by_id(self, post: Post) -> Optional[Post]:
        val = dict(self.posts.find_one({"_id": post._id}))
        if val is None:
            return None
        else:
            return convert_doc_to_post(val)

    def update_post(self, post: Post):
        val = convert_post_to_doc(post)
        return self.posts.update_one({"_id": post._id}, val)

    def delete_post(self, post: Post):
        val = convert_post_to_doc(post)
        return self.posts.delete_one({"_id": post._id})


class YandexS3:
    def __init__(self) -> None:
        session = boto3.session.Session()
        self.s3 = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net'
        )
        self.bucket = self.s3.create_bucket(Bucket=config.bucket)

    def save_object(self, string: str, hash: str):
        return self.s3.put_object(Bucket=self.bucket, Key=hash, Body=string, StorageClass='STANDARD')

    def get_object(self, hash: str):
        get_object_response = self.s3.get_object(Bucket=self.bucket, Key=hash).get('Body')
        return get_object_response.read()


db = Database()
storage = Storage()
s3 = YandexS3()
