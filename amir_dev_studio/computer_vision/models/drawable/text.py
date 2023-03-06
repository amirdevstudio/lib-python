from dataclasses import dataclass, field

import cv2
import numpy as np

from amir_dev_studio.computer_vision.models.base import Base
from amir_dev_studio.computer_vision.models.color import Color
from amir_dev_studio.computer_vision.models.drawable.configs import (
    get_default_draw_thickness,
    get_default_draw_font_scale,
    get_default_draw_color
)
from amir_dev_studio.computer_vision.models.drawable.base import Drawable
from amir_dev_studio.computer_vision.models.point import Point


@dataclass
class DrawableText(Base, Drawable[np.ndarray]):
    value: str
    position: Point

    color: Color = field(default_factory=get_default_draw_color)
    font_scale: float = field(default_factory=get_default_draw_font_scale)
    font_face: int = field(default_factory=lambda: cv2.FONT_HERSHEY_SIMPLEX)
    thickness: int = field(default_factory=get_default_draw_thickness)

    def __copy__(self):
        return DrawableText(
            self.value,
            self.position.copy(),
            self.color.copy(),
            self.font_scale,
            self.thickness
        )

    def draw_on_image(self, pixels: np.ndarray) -> np.ndarray:
        return cv2.putText(
            pixels,
            self.value,
            self.position.xy,
            self.font_face,
            self.font_scale,
            self.color.rgb,
            self.thickness
        )
