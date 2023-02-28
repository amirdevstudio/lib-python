from dataclasses import dataclass
from pathlib import Path

import cv2

from amir_dev_studio.computer_vision.enums import ColorSpaces
from amir_dev_studio.computer_vision.models.image import Image


@dataclass
class ImageFile:
    path: str | Path

    def __post_init__(self):
        self.path = Path(self.path)

    def read_image(self):
        data = cv2.imread(str(self.path))
        return Image(data, color_space=ColorSpaces.BGR)
