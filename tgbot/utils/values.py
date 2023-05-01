from typing import Dict, List, Optional

from tgbot.common_types import File, FileTypes
from tgbot.databases.redis_storage import storage


def set_value(value_name: str, value: str, user_id: str):
    key = value_name + user_id
    storage.add_value(key, value)


def get_value(value_name: str, user_id: str) -> str:
    key = value_name + user_id
    return storage.get_value(key)


def delete_value(value_name: str, user_id: str) -> str:
    key = value_name + user_id
    return storage.delete_value(key)


def add_file_to_list(file: File, user_id: str):
    key = 'list_of_values' + user_id
    value = file['file_id'] + ',' + file['file']
    storage.add_value_to_list(key, value)


def get_count_files(user_id: str) -> int:
    key = 'files' + user_id
    return storage.size_of_list(key)


def get_files(user_id: str) -> List[File]:
    key = 'files' + user_id
    values = storage.get_list_of_values(key)
    res = []
    for value in values:
        val = value.split(',')
        res.append(File(
            file_id=val[0],
            file=FileTypes(val[1])
        ))
    return res


def delete_files(user_id: str):
    key = 'list_of_values' + user_id
    storage.delete_list(key)


def add_values_to_map(map_name: str, values: Dict[str, str], user_id: str):
    name = map_name + user_id
    storage.add_values_to_map(name, values)


def get_value_from_map(map_name: str, key: str, user_id: str) -> Optional[str]:
    name = map_name + user_id
    return storage.get_value_from_map(name, key)


def delete_value_from_map(map_name: str, key: str, user_id: str):
    name = map_name + user_id
    storage.delete_value_from_map(name, key)


def get_all_values_from_map(map_name: str, user_id: str) -> Dict[str, str]:
    name = map_name + user_id
    return storage.get_map(name)


def clean_map(map_name: str, user_id: str):
    name = map_name + user_id
    storage.clean_map(name)


def add_value_to_list(list_name: str, value: str, user_id: str):
    list_name += user_id
    storage.add_value_to_list(list_name, value)


def get_list(list_name: str, user_id: str) -> List[str]:
    list_name += user_id
    return storage.get_list_of_values(list_name)


def delete_list(list_name: str, user_id: str):
    list_name += user_id
    storage.delete_list(list_name)
