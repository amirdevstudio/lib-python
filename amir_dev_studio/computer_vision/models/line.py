from dataclasses import dataclass
from typing import Optional

from amir_dev_studio.computer_vision.enums import CardinalDirections, OrdinalDirections
from amir_dev_studio.computer_vision.models.base import Model
from amir_dev_studio.computer_vision.models.color import Color
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
    def render_args_dict(self) -> dict:
        return self.extra_data.get('render_args', {})

    @property
    def color(self) -> Optional[Color]:
        return self.render_args_dict.get('color', None)

    @color.setter
    def color(self, color: Color):
        self.render_args_dict['color'] = color

    @property
    def thickness(self) -> Optional[int]:
        return self.render_args_dict.get('thickness', None)

    @thickness.setter
    def thickness(self, thickness: int):
        self.render_args_dict['thickness'] = thickness

    @property
    def slope(self) -> Number:
        return Number(
            (self.pt2.y - self.pt1.y) /
            (self.pt2.x - self.pt1.x)
        )
