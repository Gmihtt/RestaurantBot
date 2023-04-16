from tgbot.places.place import Restaurant, Place, PlaceType


def pretty_show_restaurant(rest: Restaurant) -> str:
    mid_price = ""
    if rest['mid_price'] is not None:
        mid_price = 'средний чек: ' + str(rest['mid_price']) + '\n'
    business_lunch_price = ""
    if rest['business_lunch']:
        business_lunch_price = 'цена бизнес ланча: ' + str(rest['business_lunch_price']) + '\n'
    kitchen = ""
    if rest['kitchen'] is not None:
        kitchen = 'кухня: ' + rest['kitchen'] + '\n'
    return mid_price + business_lunch_price + kitchen


def pretty_show_place(place: Place, is_admin: bool) -> str:
    print(place)
    place_id = ""
    if place['_id'] is not None:
        place_id = "" if not is_admin else "id: " + str(place['_id']) + '\n'
    name = "Название: " + place['name'] + '\n'
    place_str = ""
    place_type = ""
    if place['place_type'] == PlaceType.RESTAURANT:
        place_type = "Ресторан" + '\n'
        place_str = pretty_show_restaurant(place['place']) + '\n'
    address = "Адресс: " + place['address'] + '\n'
    telephone = "Телефон: " + place['telephone'] + '\n'
    url = "" if place['url'] is None else place['url'] + '\n'
    work_interval = "Время работы: " + place['work_interval'] + '\n'
    description = "" if place['description'] is None else '\n' + place['description'] + '\n'
    return (place_id +
            name +
            place_type +
            place_str +
            address +
            telephone +
            url +
            work_interval +
            description
            )
