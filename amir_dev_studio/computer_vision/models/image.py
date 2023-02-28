from __future__ import annotations

from dataclasses import dataclass, field

import cv2
import numpy as np

from amir_dev_studio.computer_vision.enums import ColorSpaces
from amir_dev_studio.computer_vision.models.base import BaseModel
from amir_dev_studio.computer_vision.models.circle import Circle
from amir_dev_studio.computer_vision.models.color import Color
from amir_dev_studio.computer_vision.models.line import Line
from amir_dev_studio.computer_vision.models.point import Point
from amir_dev_studio.computer_vision.models.rectangle import Rectangle


def copy_self_and_apply_method(self, fn: callable, *args, **kwargs):
    self_copy = self.__copy__()
    fn(self_copy, *args, **kwargs)
    return self_copy


@dataclass
class Image(BaseModel):
    data: np.ndarray
    color_space: ColorSpaces

    circles: list = field(default_factory=list, init=False)
    lines: list = field(default_factory=list, init=False)
    rectangles: list = field(default_factory=list, init=False)
    texts: list = field(default_factory=list, init=False)

    def __copy__(self):
        return Image(
            data=self.data.copy(),
            color_space=self.color_space
        )

    def __repr__(self):
        return f'<Image width={self.width} height={self.height} shape={self.data.shape} >'

    @property
    def width(self):
        return self.data.shape[1]

    @property
    def height(self):
        return self.data.shape[0]

    @property
    def center(self) -> Point:
        return Point(self.width / 2, self.height / 2)

    @classmethod
    def create_blank(cls, height: int, width: int, channels: int = 3) -> Image:
        return cls(
            data=np.zeros((height, width, channels), np.uint8),
            color_space=ColorSpaces.BGR
        )

    def apply_brightness_(self, value: float):
        if value > 0:
            shadow = value
            max_ = 255

        else:
            shadow = 0
            max_ = 255 + value

        alpha = (max_ - shadow) / 255
        gamma = shadow

        self.data = cv2.addWeighted(self.data, alpha, self.data, 0, gamma)

        return self
    
    def apply_color_space_conversion_(self, color_space: ColorSpaces):
        conversion_key = (self.color_space, color_space)
        conversions = {
            (ColorSpaces.BGR, ColorSpaces.GRAY): cv2.COLOR_BGR2GRAY,
            (ColorSpaces.BGR, ColorSpaces.RGB): cv2.COLOR_BGR2RGB,
        }

        if not (conversion := conversions.get(conversion_key)):
            raise Exception(f'Could not convert {self.color_space} to {color_space}')

        self.data = cv2.cvtColor(self.data, conversion)
        self.color_space = color_space

    def apply_contrast_(self, value: float):
        alpha = float(131 * (value + 127)) / (127 * (131 - value))
        gamma = 127 * (1 - alpha)
        self.data = cv2.addWeighted(self.data, alpha, self.data, 0, gamma)

    def apply_gaussian_blur_(self, kernel_size: int):
        self.data = cv2.GaussianBlur(self.data, (kernel_size, kernel_size), 0)

    def apply_grayscale_conversion_(self):
        self.apply_color_space_conversion_(ColorSpaces.GRAY)
        self.data = np.stack((self.data,) * 3, axis=-1)

    def apply_rgb_conversion_(self):
        self.apply_color_space_conversion_(ColorSpaces.RGB)

    def blank_copy(self):
        return Image.create_blank(self.height, self.width)

    def concat_horizontal_(self, image: Image):
        self.data = np.concatenate((self.data, image.data), axis=1)

    def concat_vertical_(self, image: Image):
        self.data = np.concatenate((self.data, image.data), axis=0)

    def copy(self) -> Image:
        return self.__copy__()

    def draw_circle_(self, circle: Circle, color: Color, thickness: int = 2):
        self.circles.append((circle, color, thickness))

    def draw_line_(self, line: Line, color: Color, thickness: int = 2):
        self.lines.append((line, color, thickness))

    def draw_rectangle_(self, rectangle: Rectangle, color: Color, thickness: int = 2):
        self.rectangles.append((rectangle, color, thickness))

    def draw_text_(self, text: str, position: Point, color: Color, font_scale: float = 1, thickness: int = 1):
        self.texts.append((text, position, color, font_scale, thickness))

    def iter_resized_copies(self, start, stop, count):
        diff = abs(stop - start)
        step = diff / count

        for i in range(count):
            scale = start + (step * i)
            res = self.__copy__()
            res.resize_(scale)

            yield res

    def render_circles_(self):
        for circle, color, thickness in self.circles:
            cv2.circle(
                self.data,
                circle.center.xy_ints,
                circle.radius,
                color.bgr,
                thickness=thickness
            )

    def render_lines_(self):
        for line, color, thickness in self.lines:
            cv2.line(
                self.data,
                line.pt1.xy_ints,
                line.pt2.xy_ints,
                color.bgr,
                thickness=thickness
            )

    def render_rectangles_(self):
        for rectangle, color, thickness in self.rectangles:
            cv2.rectangle(
                self.data,
                rectangle.top_left.xy_ints,
                rectangle.bottom_right.xy_ints,
                color.bgr,
                thickness=thickness
            )

    def render_text_(self, text: str, position: Point, color: Color, font_scale: float = 1, thickness: int = 1):
        cv2.putText(
            self.data,
            text,
            position.xy_ints,
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            color.bgr,
            thickness=thickness
        )

    def render_texts_(self):
        for text, position, color, font_scale, thickness in self.texts:
            cv2.putText(
                self.data,
                text,
                position.xy_ints,
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale,
                color.bgr,
                thickness=thickness
            )

    def resize_(self, scale: float):
        new_width = int(self.width * scale)
        new_height = int(self.height * scale)

        self.data = cv2.resize(
            self.data,
            (new_width, new_height),
            interpolation=cv2.INTER_AREA
        )

    def trim_top_(self, pixels: int):
        self.data = self.data[pixels:]

    def trim_bottom_(self, pixels: int):
        self.data = self.data[:-pixels]

    def trim_left_(self, pixels: int):
        self.data = self.data[:, pixels:]

    def trim_right_(self, pixels: int):
        self.data = self.data[:, :-pixels]

    def trim_(self, *args: int):
        if len(args) == 1:
            top = left = bottom = right = args[0]

        elif len(args) == 2:
            (top, bottom), (left, right) = args

        elif len(args) == 4:
            top, bottom, left, right = args

        else:
            raise Exception(f'Invalid number of arguments. Expected 1, 2 or 4. Got: {len(args)}')

        self.trim_top_(top)
        self.trim_left_(left)
        self.trim_bottom_(bottom)
        self.trim_right_(right)

    def apply_color_space_conversion(self, color_space: ColorSpaces):
        return copy_self_and_apply_method(self, self.apply_color_space_conversion_, color_space)

    def apply_contrast(self, value: float):
        return copy_self_and_apply_method(self, self.apply_contrast_, value)

    def apply_gaussian_blur(self, kernel_size: int):
        return copy_self_and_apply_method(self, self.apply_gaussian_blur_, kernel_size)

    def apply_grayscale_conversion(self):
        return copy_self_and_apply_method(self, self.apply_grayscale_conversion_)

    def apply_rgb_conversion(self):
        return copy_self_and_apply_method(self, self.apply_rgb_conversion_)

    def concat_horizontal(self, image: Image):
        return copy_self_and_apply_method(self, self.concat_horizontal_, image)

    def concat_vertical(self, image: Image):
        return copy_self_and_apply_method(self, self.concat_vertical_, image)

    def draw_circle(self, circle: Circle, color: Color, thickness: int = 2):
        return copy_self_and_apply_method(self, self.draw_circle_, circle, color, thickness)

    def draw_line(self, line: Line, color: Color, thickness: int = 2):
        return copy_self_and_apply_method(self, self.draw_line_, line, color, thickness)

    def draw_rectangle(self, rectangle: Rectangle, color: Color, thickness: int = 2):
        return copy_self_and_apply_method(self, self.draw_rectangle_, rectangle, color, thickness)

    def draw_text(self, text: str, position: Point, color: Color, font_scale: float = 1, thickness: int = 1):
        return copy_self_and_apply_method(self, self.draw_text_, text, position, color, font_scale, thickness)

    def render_circles(self):
        return copy_self_and_apply_method(self, self.render_circles_)

    def render_lines(self):
        return copy_self_and_apply_method(self, self.render_lines_)

    def render_rectangles(self):
        return copy_self_and_apply_method(self, self.render_rectangles_)

    def render_texts(self):
        return copy_self_and_apply_method(self, self.render_texts_)

    def resize(self, scale: float):
        return copy_self_and_apply_method(self, self.resize_, scale)

    def trim_top(self, pixels: int):
        return copy_self_and_apply_method(self, self.trim_top_, pixels)

    def trim_bottom(self, pixels: int):
        return copy_self_and_apply_method(self, self.trim_bottom_, pixels)

    def trim_left(self, pixels: int):
        return copy_self_and_apply_method(self, self.trim_left_, pixels)

    def trim_right(self, pixels: int):
        return copy_self_and_apply_method(self, self.trim_right_, pixels)

    def trim(self, *args: int):
        return copy_self_and_apply_method(self, self.trim_, *args)
