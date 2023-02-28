from enum import Enum, auto


class CardinalDirections(Enum):
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    UP = auto()


class ColorSpaces(Enum):
    BGR = auto()
    GRAY = auto()
    RGB = auto()
    RGBA = auto()


class OrdinalDirections(Enum):
    DOWN_LEFT = auto()
    DOWN_RIGHT = auto()
    UP_LEFT = auto()
    UP_RIGHT = auto()
