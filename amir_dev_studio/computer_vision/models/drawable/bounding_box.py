from dataclasses import dataclass

import numpy as np

from amir_dev_studio.computer_vision.models.base import Base
from amir_dev_studio.computer_vision.models.drawable.base import Drawable
from amir_dev_studio.computer_vision.models.drawable.rectangle import DrawableRectangle
from amir_dev_studio.computer_vision.models.drawable.text import DrawableText


@dataclass
class DrawableBoundingBox(Base, Drawable[np.ndarray]):
    text: DrawableText
    rect: DrawableRectangle

    def __copy__(self):
        return DrawableBoundingBox(
            self.text.copy(),
            self.rect.copy()
        )

    def draw_on_image(self, pixels: np.ndarray) -> np.ndarray:
        pixels = self.text.draw_on_image(pixels)
        pixels = self.rect.draw_on_image(pixels)
        return pixels
