from dataclasses import dataclass
from math import dist

from amir_dev_studio.computer_vision.models.base import Model


@dataclass
class Point(Model):
    x: float
    y: float

    def __copy__(self):
        return Point(self.x, self.y)

    @property
    def quadrant(self) -> int:
        if self.x > 0:
            return 1 if self.y > 0 else 4
        if self.x < 0:
            return 2 if self.y > 0 else 3
        return 0

    @property
    def xy(self):
        return self.x, self.y

    @property
    def xy_ints(self):
        return int(self.x), int(self.y)

    def translate(self, x: int = 0, y: int = 0):
        return Point(self.x + x, self.y + y)

    def distance_from(self, other: 'Point'):
        return dist(self.xy, other.xy)

    def is_above(self, other: 'Point') -> bool:
        return self.y < other.y

    def is_below(self, other: 'Point') -> bool:
        return self.y > other.y

    def is_left_of(self, other: 'Point') -> bool:
        return self.x < other.x

    def is_right_of(self, other: 'Point') -> bool:
        return self.x > other.x

    def is_bottom_left_of(self, other: 'Point') -> bool:
        return self.is_below(other) and self.is_left_of(other)

    def is_bottom_right_of(self, other: 'Point') -> bool:
        return self.is_below(other) and self.is_right_of(other)

    def is_top_left_of(self, other: 'Point') -> bool:
        return self.is_above(other) and self.is_left_of(other)

    def is_top_right_of(self, other: 'Point') -> bool:
        return self.is_above(other) and self.is_right_of(other)
