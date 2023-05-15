from typing import Optional

import pymongo
from bson import ObjectId
from pymongo import MongoClient

from tgbot import config
import logging

from tgbot.posts import post


class DatabaseOld:
    def __init__(self) -> None:
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[config.mongo_database]  # init db
        self.posts = self.db[config.posts_collection]

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
        if val is None:
            return None
        else:
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


db = DatabaseOld()
