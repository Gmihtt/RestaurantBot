from tgbot.places.place import Restaurant, Place, PlaceType


def pretty_show_restaurant(rest: Restaurant) -> str:
    mid_price = ""
    if rest.get('mid_price') is not None:
        mid_price = 'средний чек: ' + str(rest['mid_price']) + '\n'
    if rest['business_lunch']:
        business_lunch_price = 'цена бизнес-ланча: ' + str(rest['business_lunch_price']) + '\n'
    else:
        business_lunch_price = "бизнес-ланча: нет" + '\n'
    kitchen = ""
    if rest.get('kitchens') is not None:
        kitchens = str(rest['kitchens'])[1:-1].split(',')
        kitchen = 'кухни: '
        for k in kitchens:
            kitchen += k
    if rest['vegan']:
        vegan = 'веганская еда: есть' + '\n'
    else:
        vegan = "веганска еда: нет" + '\n'
    return mid_price + business_lunch_price + kitchen + vegan


def pretty_show_place(place: Place) -> str:
    print(place)
    name = "Название: " + place['name'] + '\n'
    place_str = ""
    place_type = ""
    if place['place_type'] == PlaceType.Restaurant:
        place_type = "Ресторан" + '\n'
        if place.get('place') is not None:
            place_str = pretty_show_restaurant(place['place']) + '\n'
    address = "Адрес: " + place['address'] + '\n'
    work_interval = ""
    if place.get('work_interval') is not None:
        work_interval = "Время работы: " + place['work_interval'] + '\n'
    description = ""
    if place.get('description') is not None:
        description = place['description'] + '\n'
    return (name +
            place_type +
            place_str +
            address +
            work_interval +
            description
            )
