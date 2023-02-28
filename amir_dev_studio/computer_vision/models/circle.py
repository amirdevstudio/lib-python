from dataclasses import dataclass
from math import acos, cos, pi, sin
from typing import Optional

from amir_dev_studio.computer_vision.models.base import RenderableShape
from amir_dev_studio.computer_vision.models.color import Color
from amir_dev_studio.computer_vision.models.point import Point


@dataclass
class Circle(RenderableShape):
    center: Point
    radius: float

    @property
    def circumference(self) -> float:
        return self.radius * 2 * pi

    @property
    def max_x(self) -> Point:
        return Point(self.center.x + self.radius, self.center.y)

    @property
    def max_y(self) -> Point:
        return Point(self.center.x, self.center.y + self.radius)

    @property
    def min_x(self) -> Point:
        return Point(self.center.x - self.radius, self.center.y)

    @property
    def min_y(self) -> Point:
        return Point(self.center.x, self.center.y - self.radius)

    @property
    def color(self) -> Optional[Color]:
        return self.render_args.get('color')

    @color.setter
    def color(self, value: Color):
        self.render_args['color'] = value

    @property
    def thickness(self) -> Optional[int]:
        return self.render_args.get('thickness')

    @thickness.setter
    def thickness(self, value: int):
        self.render_args['thickness'] = value

    @classmethod
    def from_xyr(cls, x: float, y: float, radius: float):
        center = Point(x, y)
        return cls(center, radius)

    def to_xyr(self) -> tuple[float, float, float]:
        return self.center.x, self.center.y, self.radius

    def radians_between(self, pt1: Point, pt2: Point) -> float:
        c = pt1.distance_from(pt2)
        a = b = self.radius
        return acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))

    def degrees_between(self, pt1: Point, pt2: Point) -> float:
        return self.radians_between(pt1, pt2) * (180 / pi)

    def arc_length_between(self, pt1: Point, pt2: Point):
        return self.radians_between(pt1, pt2) * self.radius

    def list_points_on_circumference(self, steps: int, clockwise: bool = True) -> list[Point]:
        radians_per_step = (2 * pi) / steps
        points = []

        for step in range(0, steps + 1):
            x = self.center.x + self.radius * cos(step * radians_per_step)
            y = self.center.y + self.radius * sin(step * radians_per_step)
            point = Point(x, y)
            points.append(point)

        if not clockwise:
            points.reverse()

        return points
