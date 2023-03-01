from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

import cv2
import numpy as np

from amir_dev_studio.computer_vision.enums import ColorSpaces
from amir_dev_studio.computer_vision.models.base import Model
from amir_dev_studio.computer_vision.models.bbox_annotation import BoundingBoxAnnotation
from amir_dev_studio.computer_vision.models.circle import RenderableCircle
from amir_dev_studio.computer_vision.models.line import RenderableLine
from amir_dev_studio.computer_vision.models.point import Point
from amir_dev_studio.computer_vision.models.rectangle import RenderableRectangle
from amir_dev_studio.computer_vision.models.text import RenderableText


@dataclass
class Image(Model):
    color_space: ColorSpaces
    pixels: np.ndarray
    name: str = 'Untitled'
    
    bounding_boxes: List[BoundingBoxAnnotation] = field(default_factory=list)
    circles: List[RenderableCircle] = field(default_factory=list)
    lines: List[RenderableLine] = field(default_factory=list)
    rectangles: List[RenderableRectangle] = field(default_factory=list)
    texts: List[RenderableText] = field(default_factory=list)

    def __copy__(self):
        return Image(
            color_space=self.color_space,
            name=self.name,
            pixels=self.pixels.copy(),
            circles=self.circles.copy(),
            lines=self.lines.copy(),
            rectangles=self.rectangles.copy(),
            texts=self.texts.copy()
        )

    def __repr__(self):
        return f'<Image width={self.width} height={self.height} shape={self.pixels.shape} >'

    @property
    def width(self):
        return self.pixels.shape[1]

    @property
    def height(self):
        return self.pixels.shape[0]

    @property
    def center(self) -> Point:
        return Point(self.width / 2, self.height / 2)

    @classmethod
    def create_blank(cls, height: int, width: int, channels: int = 3) -> Image:
        return cls(
            pixels=np.zeros((height, width, channels), np.uint8),
            color_space=ColorSpaces.BGR
        )

    @classmethod
    def create_from_pixels(cls, pixels: np.ndarray, color_space: ColorSpaces, *args, **kwargs) -> Image:
        return cls(
            pixels=pixels,
            color_space=color_space,
            *args,
            **kwargs
        )

    @classmethod
    def create_from_path(cls, path: str, *args, **kwargs) -> Image:
        pixels = cv2.imread(path)
        return cls.create_from_pixels(
            pixels,
            ColorSpaces.BGR,
            *args,
            **kwargs
        )

    def add_bounding_box(self, bounding_box: BoundingBoxAnnotation):
        self.bounding_boxes.append(bounding_box)

    def add_circle(self, circle: RenderableCircle):
        self.circles.append(circle)

    def add_line(self, line: RenderableLine):
        self.lines.append(line)

    def add_rectangle(self, rectangle: RenderableRectangle):
        self.rectangles.append(rectangle)

    def add_text(self, text: RenderableText):
        self.texts.append(text)

    def apply_brightness(self, value: float):
        if value > 0:
            shadow = value
            max_ = 255

        else:
            shadow = 0
            max_ = 255 + value

        alpha = (max_ - shadow) / 255
        gamma = shadow

        self.pixels = cv2.addWeighted(self.pixels, alpha, self.pixels, 0, gamma)

        return self
    
    def apply_color_space_conversion(self, color_space: ColorSpaces):
        conversion_key = (self.color_space, color_space)
        conversions = {
            (ColorSpaces.BGR, ColorSpaces.GRAY): cv2.COLOR_BGR2GRAY,
            (ColorSpaces.BGR, ColorSpaces.RGB): cv2.COLOR_BGR2RGB,
        }

        if not (conversion := conversions.get(conversion_key)):
            raise Exception(f'Could not convert {self.color_space} to {color_space}')

        self.pixels = cv2.cvtColor(self.pixels, conversion)
        self.color_space = color_space

    def apply_contrast(self, value: float):
        alpha = float(131 * (value + 127)) / (127 * (131 - value))
        gamma = 127 * (1 - alpha)
        self.pixels = cv2.addWeighted(self.pixels, alpha, self.pixels, 0, gamma)

    def apply_gaussian_blur(self, kernel_size: int):
        self.pixels = cv2.GaussianBlur(self.pixels, (kernel_size, kernel_size), 0)

    def apply_grayscale_conversion(self):
        self.apply_color_space_conversion(ColorSpaces.GRAY)
        self.pixels = np.stack((self.pixels,) * 3, axis=-1)

    def apply_rgb_conversion(self):
        self.apply_color_space_conversion(ColorSpaces.RGB)

    def blank_copy(self):
        return self.__class__.create_blank(self.width, self.height)

    def concat_horizontal(self, image: Image):
        self.pixels = np.concatenate((self.pixels, image.pixels), axis=1)

    def concat_vertical(self, image: Image):
        self.pixels = np.concatenate((self.pixels, image.pixels), axis=0)

    def copy(self) -> Image:
        return self.__copy__()

    def iter_resized_copies(self, start, stop, count):
        step = abs(stop - start) / count

        for i in range(count):
            scale = start + (step * i)
            copy = self.copy()
            copy.resize(scale)
            yield copy

    def render_circles(self):
        for circle in self.circles:
            cv2.circle(
                self.pixels,
                circle.center.xy_ints,
                circle.radius,
                circle.color.bgr,
                thickness=circle.thickness
            )

    def render_lines(self):
        for line in self.lines:
            cv2.line(
                self.pixels,
                line.pt1.xy_ints,
                line.pt2.xy_ints,
                line.color.bgr,
                thickness=line.thickness
            )

    def render_rectangles(self):
        for rectangle in self.rectangles:
            cv2.rectangle(
                self.pixels,
                rectangle.top_left.xy_ints,
                rectangle.bottom_right.xy_ints,
                rectangle.color.bgr,
                thickness=rectangle.thickness
            )

    def render_texts(self):
        for text in self.texts:
            cv2.putText(
                self.pixels,
                text.value,
                text.position.xy_ints,
                cv2.FONT_HERSHEY_SIMPLEX,
                text.font_scale,
                text.color.bgr,
                thickness=text.thickness
            )

    def resize(self, scale: float):
        new_width = int(self.width * scale)
        new_height = int(self.height * scale)

        self.pixels = cv2.resize(
            self.pixels,
            (new_width, new_height),
            interpolation=cv2.INTER_AREA
        )

    def show(self, title: str = None, wait_key: int = 0):
        title = title or self.name
        cv2.imshow(title, self.pixels)
        cv2.waitKey(wait_key)
        cv2.destroyWindow(title)

    def trim_top(self, pixels: int):
        self.pixels = self.pixels[pixels:]

    def trim_bottom(self, pixels: int):
        self.pixels = self.pixels[:-pixels]

    def trim_left(self, pixels: int):
        self.pixels = self.pixels[:, pixels:]

    def trim_right(self, pixels: int):
        self.pixels = self.pixels[:, :-pixels]

    def trim(self, *args: int):
        if len(args) == 1:
            top = left = bottom = right = args[0]

        elif len(args) == 2:
            (top, bottom), (left, right) = args

        elif len(args) == 4:
            top, bottom, left, right = args

        else:
            raise Exception(f'Invalid number of arguments. Expected 1, 2 or 4. Got: {len(args)}')

        self.trim_top(top)
        self.trim_left(left)
        self.trim_bottom(bottom)
        self.trim_right(right)
