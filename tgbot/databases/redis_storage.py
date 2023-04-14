from typing import Optional, Dict
import redis


class Storage:
    def __init__(self) -> None:
        self.r = redis.StrictRedis(host="localhost", port=6379, password="", decode_responses=True)
        keys = self.r.keys('*')
        if keys:
            self.r.delete(*keys)

    def add_val(self, key: str, val: str) -> bool:
        return self.r.set(key, val)

    def get_val(self, key: str) -> Optional[str]:
        return self.r.get(key)

    def pop_val(self, key: str) -> Optional[str]:
        res = self.get_val(key)
        if res is not None:
            self.delete_val(key)
        return res

    def delete_val(self, key: str):
        self.r.delete(key)

    def add_map(self, name: str, vals: Dict[str, str]):
        self.r.hset(name=name, mapping=vals)

    def get_val_of_map(self, name, key):
        self.r.hget(name=name, key=key)

    def get_map(self, name):
        return self.r.hgetall(name=name)


storage = Storage()
