from typing import Dict, List

from tgbot.common_types import File, FileTypes
from tgbot.databases.redis_storage import storage


def set_value(value: str, user_id: str):
    key = 'value' + user_id
    storage.add_value(key, value)


def get_value(user_id: str) -> str:
    key = 'value' + user_id
    return storage.get_value(key)


def add_file_to_list(file: File, user_id: str):
    key = 'list_of_values' + user_id
    value = file['file_id'] + ',' + file['file']
    storage.add_value_to_list(key, value)


def get_count_files(user_id: str) -> int:
    key = 'list_of_values' + user_id
    return storage.size_of_list(key)


def get_files(user_id: str) -> List[File]:
    key = 'list_of_values' + user_id
    values = storage.get_list_of_values(key)
    res = []
    for value in values:
        val = value.split(',')
        res.append(File(
            file_id=val[0],
            file=FileTypes[val[1]]
        ))
    return res


def delete_files(user_id: str):
    key = 'list_of_values' + user_id
    storage.delete_list(key)


def add_values_to_map(values: Dict[str, str], user_id: str):
    name = 'map_of_value' + user_id
    storage.add_values_to_map(name, values)


def get_all_values_from_map(user_id: str) -> Dict[str, str]:
    name = 'map_of_value' + user_id
    return storage.get_map(name)


def clean_map(user_id: str):
    name = 'map_of_value' + user_id
    clean_map(name)
