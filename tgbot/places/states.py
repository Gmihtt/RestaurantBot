from strenum import StrEnum


class PlaceStates(StrEnum):
    Search = "search"
    Edit = "edit"
    AddRestaurantInfo = "add_restaurant_info"
    AddFiles = "add_files"
    AddDescription = "add_description"
    Approve = "approve"
    Push = "push"
    ShowPlaces = "show_places"
    ShowPlace = "show_place"
    FavoritePlaces = "favorite_places"
    FavoriteDelete = "favorite_delete"
