from typing import Optional

from tgbot.places.place import Restaurant, Place, PlaceType


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
    if rest['vegan']:
        vegan = 'Веганская еда: <i>Есть</i>' + '\n'
    business = ""
    if "Бизнес-ланч" in rest['features']:
        business = "Бизнес ланч: <i>Есть</i>" + '\n'
    terrace = ""
    if "Летняя веранда" in rest['features']:
        terrace = "Терраса: <i>Есть</i>" + '\n'
    hookah = ""
    if "Кальян-бар" in rest['features']:
        hookah = "Кальянная зона: <i>Есть</i>" + '\n'

    cart_pay = ""
    if "Оплата картой" in rest['features']:
        cart_pay = "Оплата картой: <i>Есть</i>"

    return rating + mid_price + kitchen + vegan + business + terrace + hookah + cart_pay


def pretty_show_place(place: Place, distance: Optional[float]) -> str:
    name = '<b>' + place['name'] + '</b>\n\n'

    dist = ""
    if distance is not None:
        dist = "Расстояние до места: <i>" + str(round(distance, 1)) + " км.</i>\n"

    place_str = ""
    if place['place_type'] == PlaceType.Restaurant:
        if place.get('place') is not None:
            place_str = pretty_show_restaurant(place['place']) + '\n\n'

    place_adr = place['address'].split(',')[1:]
    address = "Адрес: <i>"
    for i, adr in enumerate(place_adr):
        if i != len(place_adr) - 1:
            address += adr + ', '
        else:
            address += adr
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
            place_str +
            address +
            work_interval +
            description
            )
