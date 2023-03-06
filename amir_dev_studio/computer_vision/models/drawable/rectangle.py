from dataclasses import dataclass, field

import cv2
import numpy as np

from amir_dev_studio.computer_vision.models.base import Base
from amir_dev_studio.computer_vision.models.color import Color
from amir_dev_studio.computer_vision.models.drawable.base import Drawable
from amir_dev_studio.computer_vision.models.drawable.configs import get_default_draw_thickness, get_default_draw_color
from amir_dev_studio.computer_vision.models.point import Point


@dataclass
class Rectangle(Base):
    """
    A rectangle defined by two opposite corners.
    """
    pt1: Point
    pt2: Point

    def __copy__(self):
        return Rectangle(self.pt1, self.pt2)

    def __post_init__(self):
        assert self.pt1.xy != self.pt2.xy, 'Rectangle cannot have zero area'
        assert self.pt1.x != self.pt2.x, 'Rectangle width cannot be 0'
        assert self.pt1.y != self.pt2.y, 'Rectangle height cannot be 0'

    def __repr__(self):
        return f'Rectangle({self.top_left.xy}, {self.bottom_right.xy})'

    @property
    def bottom(self) -> float:
        return self.bottom_right.y

    @property
    def bottom_right(self) -> Point:
        return Point(
            max(self.pt1.x, self.pt2.x),
            max(self.pt1.y, self.pt2.y)
        )

    @property
    def center(self) -> Point:
        return Point(
            self.top_left.x + self.width / 2,
            self.top_left.y + self.height / 2
        )

    @property
    def height(self):
        return self.bottom_right.y - self.top_left.y

    @property
    def left(self) -> float:
        return self.top_left.x

    @property
    def right(self) -> float:
        return self.bottom_right.x

    @property
    def top(self) -> float:
        return self.top_left.y

    @property
    def top_left(self) -> Point:
        return Point(
            min(self.pt1.x, self.pt2.x),
            min(self.pt1.y, self.pt2.y)
        )

    @property
    def width(self) -> float:
        return self.bottom_right.x - self.top_left.x

    @classmethod
    def from_coco_bbox(cls, x: float, y: float, width: float, height: float):
        return cls.from_ltwh(x, y, width, height)

    @classmethod
    def from_ltrb(cls, left: float, top: float, right: float, bottom: float):
        return cls(
            Point(left, top),
            Point(right, bottom)
        )

    @classmethod
    def from_ltwh(cls, left: float, top: float, width: float, height: float):
        return cls(
            Point(left, top),
            Point(left + width, top + height)
        )

    @classmethod
    def from_tlbr(cls, top: float, left: float, bottom: float, right: float):
        return cls(
            Point(left, top),
            Point(right, bottom)
        )

    @classmethod
    def from_xywh(cls, x: int, y: int, width: int, height: int):
        return cls(
            Point(x, y),
            Point(x + width, y + height)
        )

    @classmethod
    def from_yolo_bbox(cls, x: float, y: float, width: float, height: float, image_width: int, image_height: int):
        return cls.from_ltwh(
            x * image_width - width * image_width / 2,
            y * image_height - height * image_height / 2,
            width * image_width,
            height * image_height
        )

    def contains(self, other: 'Rectangle') -> bool:
        return (
            self.left <= other.left and
            self.right >= other.right and
            self.top <= other.top and
            self.bottom >= other.bottom
        )

    def get_random_point(self) -> Point:
        return Point(
            np.random.uniform(self.left + 3, self.right - 3),
            np.random.uniform(self.top + 3, self.bottom - 3)
        )

    def to_coco_bbox(self) -> tuple[float, float, float, float]:
        return self.top_left.x, self.top_left.y, self.width, self.height

    def to_tlbr(self) -> tuple[tuple[int, int], tuple[int, int]]:
        return self.top_left.xy, self.bottom_right.xy

    def to_xywh(self) -> tuple[float, float, float, float]:
        return self.top_left.x, self.top_left.y, self.width, self.height

    def to_yolo_bbox(self, image_width: int, image_height: int) -> tuple[float, float, float, float]:
        return (
            self.center.x / image_width,
            self.center.y / image_height,
            self.width / image_width,
            self.height / image_height
        )


@dataclass
class DrawableRectangle(Rectangle, Drawable[np.ndarray]):
    color: Color = field(default_factory=get_default_draw_color)
    thickness: int = field(default_factory=get_default_draw_thickness)

    def __copy__(self):
        return DrawableRectangle(
            self.pt1.copy(),
            self.pt2.copy(),
            self.color.copy(),
            self.thickness
        )

    def draw_on_image(self, pixels: np.ndarray) -> np.ndarray:
        return cv2.rectangle(
            pixels,
            self.top_left.xy,
            self.bottom_right.xy,
            self.color.rgb,
            self.thickness
        )

