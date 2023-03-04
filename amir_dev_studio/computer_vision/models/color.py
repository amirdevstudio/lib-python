from dataclasses import dataclass

from amir_dev_studio.computer_vision.models.base import Base


@dataclass
class Color(Base):
    b: int
    g: int
    r: int

    def __copy__(self):
        return Color(self.b, self.g, self.r)

    @property
    def bgr(self):
        return self.b, self.g, self.r

    @property
    def rgb(self):
        return self.r, self.g, self.b
