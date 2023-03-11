from dataclasses import dataclass

import matplotlib

from amir_dev_studio.computer_vision.models.base import Base


@dataclass
class Color(Base):
    b: float | int
    g: float | int
    r: float | int

    def __copy__(self):
        return Color(self.b, self.g, self.r)

    @property
    def bgr(self):
        return self.b, self.g, self.r

    @property
    def rgb(self):
        return self.r, self.g, self.b

    @classmethod
    def from_hex(cls, hex_color: str):
        rgb = matplotlib.colors.to_rgb(hex_color)
        rgb = [int(x * 255) for x in rgb]
        return cls(*rgb[::-1])

    def to_hex(self):
        rgb = [x / 255 for x in self.rgb]
        return matplotlib.colors.to_hex(rgb)

    def add_tint(self, tint: float):
        self.b = min(float(255), self.b + tint)
        self.g = min(float(255), self.g + tint)
        self.r = min(float(255), self.r + tint)

    def add_shade(self, shade: float):
        self.b = max(float(0), self.b - shade)
        self.g = max(float(0), self.g - shade)
        self.r = max(float(0), self.r - shade)
