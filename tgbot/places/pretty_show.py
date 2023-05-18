from typing import Optional

from tgbot.places.place import Restaurant, Place, PlaceType


def pretty_show_restaurant(rest: Restaurant) -> str:
    rating = ""
    if rest.get('rating') is not None:
        rating = "Рейтинг заведения: " + str(round(rest['rating'], 1)) + "/5.0\n"

    mid_price = ""
    if rest.get('mid_price') is not None:
        mid_price = 'Cредний чек: ' + str(rest['mid_price']) + '\n'
    kitchen = ""
    if rest.get('kitchens') is not None:
        kitchens = rest['kitchens']
        kitchen = "кухни: "
        for k in kitchens[0:5]:
            if k not in ["вегетарианская", "веганская"]:
                kitchen += k + ', '
        kitchen += '\n\n'
    vegan = ""
    if rest['vegan']:
        vegan = 'Веганская еда: Есть' + '\n'
    business = ""
    if "Бизнес-ланч" in rest['features']:
        business = "Бизнес ланч: Есть" + '\n'
    terrace = ""
    if "Летняя веранда" in rest['features']:
        terrace = "Терраса: Есть" + '\n'
    hookah = ""
    if "Кальян-бар" in rest['features']:
        hookah = "Кальянная зона: Есть" + '\n'

    cart_pay = ""
    if "Оплата картой" in rest['features']:
        cart_pay = "Оплата картой: Есть"

    return rating + mid_price + kitchen + vegan + business + terrace + hookah + cart_pay


def pretty_show_place(place: Place, distance: Optional[float]) -> str:
    name = place['name'] + '\n\n'

    dist = ""
    if distance is not None:
        dist = "Расстояние до места: " + str(distance) + "км\n"

    place_str = ""
    if place['place_type'] == PlaceType.Restaurant:
        if place.get('place') is not None:
            place_str = pretty_show_restaurant(place['place']) + '\n'

    address = "Адрес: " + place['address'] + '\n\n'

    work_interval = ""
    if place.get('work_interval') is not None:
        work_interval = "Время работы: \n"
        for work_int in place['work_interval'].split(';'):
            work_interval += "      " + work_int.strip() + "\n"

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
