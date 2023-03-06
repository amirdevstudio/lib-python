from dataclasses import dataclass, field
from math import acos, cos, pi, sin

import cv2
import numpy as np

from amir_dev_studio.computer_vision.models.base import Base
from amir_dev_studio.computer_vision.models.color import Color
from amir_dev_studio.computer_vision.models.drawable.base import Drawable
from amir_dev_studio.computer_vision.models.drawable.configs import get_default_draw_color, get_default_draw_thickness
from amir_dev_studio.computer_vision.models.point import Point


@dataclass
class Circle(Base):
    center: Point
    radius: float

    def __copy__(self):
        return Circle(
            self.center.copy(),
            self.radius
        )

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

    @classmethod
    def from_xyr(cls, x: float, y: float, radius: float):
        center = Point(x, y)
        return cls(center, radius)

    def arc_length_between(self, pt1: Point, pt2: Point):
        return self.radians_between(pt1, pt2) * self.radius

    def degrees_between(self, pt1: Point, pt2: Point) -> float:
        return self.radians_between(pt1, pt2) * (180 / pi)

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

    def radians_between(self, pt1: Point, pt2: Point) -> float:
        c = pt1.distance_from(pt2)
        a = b = self.radius
        return acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))

    def to_xyr(self) -> tuple[float, float, float]:
        return self.center.x, self.center.y, self.radius


@dataclass
class DrawableCircle(Circle, Drawable[np.ndarray]):
    color: Color = field(default_factory=get_default_draw_color)
    thickness: int = field(default_factory=get_default_draw_thickness)

    def __copy__(self):
        return DrawableCircle(
            self.center,
            self.radius,
            self.color,
            self.thickness
        )

    def draw_on_image(self, pixels: np.ndarray) -> np.ndarray:
        return cv2.circle(
            pixels,
            self.center.xy_ints,
            self.radius,
            self.color.bgr,
            self.thickness,
        )
