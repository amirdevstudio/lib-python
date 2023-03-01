from dataclasses import dataclass, field

from amir_dev_studio.computer_vision.enums import CardinalDirections, OrdinalDirections
from amir_dev_studio.computer_vision.models.base import Model
from amir_dev_studio.computer_vision.models.color import Color
from amir_dev_studio.computer_vision.models.configs import get_default_render_color, get_default_render_thickness
from amir_dev_studio.computer_vision.models.point import Point
from amir_dev_studio.extended_datatypes import Number


@dataclass
class Line(Model):
    pt1: Point
    pt2: Point

    @property
    def cardinal_direction(self):
        if self.pt2.is_left_of(self.pt1):
            return CardinalDirections.LEFT
        if self.pt2.is_right_of(self.pt1):
            return CardinalDirections.RIGHT
        if self.pt2.is_above(self.pt1):
            return CardinalDirections.UP
        if self.pt2.is_below(self.pt1):
            return CardinalDirections.DOWN

    @property
    def center(self) -> Point:
        return Point(
            (self.pt1.x + self.pt2.x) // 2,
            (self.pt1.y + self.pt2.y) // 2
        )

    @property
    def direction(self) -> tuple[CardinalDirections, OrdinalDirections]:
        return self.cardinal_direction, self.ordinal_direction

    @property
    def length(self) -> float:
        return self.pt1.distance_from(self.pt2)

    @property
    def ordinal_direction(self):
        if self.pt2.is_top_left_of(self.pt1):
            return OrdinalDirections.UP_LEFT
        if self.pt2.is_top_right_of(self.pt1):
            return OrdinalDirections.UP_RIGHT
        if self.pt2.is_bottom_left_of(self.pt1):
            return OrdinalDirections.DOWN_LEFT
        if self.pt2.is_bottom_right_of(self.pt1):
            return OrdinalDirections.DOWN_RIGHT

    @property
    def slope(self) -> Number:
        return Number(
            (self.pt2.y - self.pt1.y) /
            (self.pt2.x - self.pt1.x)
        )


@dataclass
class RenderableLine(Line):
    color: Color
    thickness: Number

    @classmethod
    def from_line(cls, line: Line, color: Color = None, thickness: Number = None):
        return cls(
            line.pt1,
            line.pt2,
            color or get_default_render_color(),
            thickness or get_default_render_thickness()
        )
