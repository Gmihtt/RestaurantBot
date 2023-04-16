from enum import auto
from strenum import StrEnum


class PostStates(StrEnum):
    Name = auto()
    Body = auto()
    Files = auto()
    Approve = auto()
    Push = auto()
    Find = auto()
    Show = auto()
