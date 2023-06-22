from typing import Optional

from tgbot.places.place import Restaurant, Place, PlaceType
from tgbot.utils.functions import create_metre_str


def pretty_show_restaurant(rest: Restaurant) -> str:
    rating = ""
    if rest.get('rating') is not None:
        rating = "Рейтинг заведения: <i>" + str(round(rest['rating'], 1)) + "/5.0</i>\n"

    mid_price = ""
    if rest.get('mid_price') is not None:
        mid_price = 'Cредний чек: <i>' + str(int(rest['mid_price'])) + ' руб.</i>\n'
    kitchen = ""
    if rest.get('kitchens') is not None and rest.get('kitchens') != []:
        kitchens = rest['kitchens']
        kitchen = "Кухни: <i>"
        for i, k in enumerate(kitchens[0:5]):
            if k not in ["вегетарианская", "веганская"]:
                if i == len(kitchens[0:5]) - 1:
                    kitchen += k
                else:
                    kitchen += k + ', '
        kitchen += '</i>\n\n'
    vegan = ""
    if rest.get('vegan') is not None and rest.get('vegan'):
        vegan = 'Веганская еда: <i>Да</i>' + '\n'
    business = ""
    if "Бизнес-ланч" in rest['features']:
        business = "Бизнес ланч: <i>Да</i>" + '\n'
    terrace = ""
    if "Летняя веранда" in rest['features']:
        terrace = "Терраса: <i>Да</i>" + '\n'
    hookah = ""
    if "Кальян-бар" in rest['features']:
        hookah = "Кальянная зона: <i>Да</i>" + '\n'

    cart_pay = ""
    if "Оплата картой" in rest['features']:
        cart_pay = "Оплата картой: <i>Да</i>"

    return rating + mid_price + kitchen + vegan + business + terrace + hookah + cart_pay


def pretty_show_place(place: Place, distance: Optional[float]) -> str:
    name = '<b>' + place['name'] + '</b>\n\n'

    place_types = ""
    if place.get('place_types') is not None and place.get('place_types') != []:
        place_types = "Тип заведения: <i>"
        for i, p_t in enumerate(place['place_types']):
            place_types += pretty_show_place_type(PlaceType(p_t))
            if i != len(place['place_types']) - 1:
                place_types += ", "
        place_types += "</i>\n\n"

    dist = ""
    if distance is not None:
        dist = "Расстояние до места: <i>"
        if distance < 1:
            distance = int(round(distance, 4) * 1000)
            dist += create_metre_str(distance) + "</i>\n"
        else:
            dist += str(round(distance, 1)) + " км.</i>\n"
        dist += "\n"

    place_str = ""
    if place.get('place') is not None:
        res = pretty_show_restaurant(place['place'])
        if res != "":
            place_str = pretty_show_restaurant(place['place']) + '\n'

    place_adr = place['address'].split(',')[1:]
    address = "Адрес: <i>"
    for i, adr in enumerate(place_adr):
        address += adr
        if i != len(place_adr) - 1:
            address += ', '
    address += '</i>\n\n'

    work_interval = ""
    if place.get('work_interval') is not None:
        work_interval = "Время работы: <i>\n"
        for work_int in place['work_interval'].split(';'):
            work_interval += work_int.strip() + "\n"
        work_interval += '</i>'

    description = ""
    if place.get('description') is not None:
        description = place['description'] + '\n'

    return (name +
            dist +
            place_types +
            place_str +
            address +
            work_interval +
            description
            )


def pretty_show_place_type(p_t: PlaceType):
    if p_t == PlaceType.Restaurant:
        return "Ресторан"
    if p_t == PlaceType.Bar:
        return "Бар"
    if p_t == PlaceType.Cafe:
        return "Кафе"
    if p_t == PlaceType.Lounge:
        return "Lounge-Бар"
    if p_t == PlaceType.Coffee:
        return "Кофейня"
    if p_t == PlaceType.Bakery:
        return "Пекарня"
