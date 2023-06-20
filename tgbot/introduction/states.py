from strenum import StrEnum


class IntroStates(StrEnum):
    Welcome = "welcome"
    MainMenu = "main_menu"
    AdminMenu = "admin_menu"
    Filters = "filters"
    DropFilters = "drop_filters"
    Kitchens = "kitchens"
    MidPrice = "mid_price"
    Rating = "rating"
    Help = "help"
    Statistics = "statistics"
    DeepLink = "deeplink"
    Cities = "cities"
    PlaceTypes = "place_types"
