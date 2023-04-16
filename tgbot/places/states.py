from enum import auto
from strenum import StrEnum


class PlaceStates(StrEnum):
    AddInfo = auto()
    AddType = auto()
    AddRestaurantInfo = auto()
    AddFiles = auto()
    AddDescription = auto()
    AddCity = auto()
    Push = auto()
    ShowPlaces = auto()
    ShowPlace = auto()
    Delete = auto()
    Edit = auto()
