from tgbot.places.place import Restaurant, Place, PlaceType


def pretty_show_restaurant(rest: Restaurant) -> str:
    mid_price = ""
    if rest.get('mid_price') is not None:
        mid_price = 'средний чек: ' + str(rest['mid_price']) + '\n'
    kitchen = ""
    if rest.get('kitchens') is not None:
        kitchens = rest['kitchens']
        kitchen = "кухни: "
        print(kitchens)
        for k in kitchens:
            kitchen += k + ' '
        kitchen += '\n'
    vegan = ""
    if rest['vegan']:
        vegan = 'веганская еда: есть' + '\n'
    business = ""
    if "Бизнес-ланч" in rest['features']:
        business = "бизнес ланч: есть" + '\n'
    terrace = ""
    if "Летняя веранда" in rest['features']:
        terrace = "терраса: есть" + '\n'
    else:
        vegan = "веганска еда: нет" + '\n'
    return mid_price + kitchen + vegan + business + terrace


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
        work_interval = "Время работы: \n"
        for work_int in place['work_interval'].split(';'):
            work_interval += "      " + work_int.strip() + "\n"
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
