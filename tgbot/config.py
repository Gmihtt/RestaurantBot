import json


def read_json(file_name: str):
    with open(file_name, 'r') as filehandle:
        text = filehandle.read()
    return json.loads(text)


def get_cities():
    d = read_json("config.json")
    return set(d['cities'])


def get_kitchens():
    d = read_json("config.json")
    return set(d['kitchens'])


def get_places_types():
    d = read_json("config.json")
    return set(d['place_types'])


TOKEN = '5997480587:AAHDMpfgj-sUXkjfnES_umWbLgQU1AR4H_s'
mongo_database = 'tgbot'
places_collection = 'places'
users_collection = 'users'
admins_collection = 'admins'
posts_collection = 'posts'
statistics_collection = 'statistics'
support = 'https://t.me/durahan'
username = "dAKB4phxFx"
password = "EIamC1W3jw"
bucket = "gmihtt-tgbot"
main_admins = {381873540, 138769502}
photos_path = "photos"
max_distance = 5

cities = sorted(get_cities())
kitchens = sorted(get_kitchens())
places_types = sorted(get_places_types())
