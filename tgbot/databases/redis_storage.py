from typing import Optional, Dict
import redis


class Storage:
    def __init__(self) -> None:
        self.r = redis.StrictRedis(host="localhost", port=6379, password="", decode_responses=True)
        keys = self.r.keys('*')
        if keys:
            self.r.delete(*keys)

    def clean_redis(self):
        keys = self.r.keys('*')
        if keys:
            self.r.delete(*keys)

    def add_value(self, key: str, val: str) -> bool:
        return self.r.set(key, val)

    def get_value(self, key: str) -> Optional[str]:
        return self.r.get(key)

    def delete_value(self, key: str):
        keys = [key]
        if keys:
            return self.r.delete(*keys)

    def add_value_to_list(self, key: str, value: str):
        self.r.lpush(key, value)

    def size_of_list(self, key: str):
        return self.r.llen(key)

    def get_list_of_values(self, key: str):
        size = self.size_of_list(key)
        print(size)
        if size == 0:
            return []
        else:
            return self.r.lrange(key, 0, size - 1)

    def delete_list(self, key: str):
        size = self.size_of_list(key)
        self.r.lpop(key, size)

    def add_values_to_map(self, name: str, vals: Dict[str, str]):
        self.r.hset(name=name, mapping=vals)

    def get_value_from_map(self, name: str, key: str):
        return self.r.hget(name, key)

    def delete_value_from_map(self, name, key):
        keys = [key]
        if keys:
            self.r.hdel(name, *keys)

    def get_map(self, name):
        return self.r.hgetall(name=name)

    def clean_map(self, name):
        keys = self.r.hkeys(name)
        if keys:
            self.r.hdel(name, *keys)


storage = Storage()
