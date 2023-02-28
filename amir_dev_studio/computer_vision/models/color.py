from dataclasses import dataclass


@dataclass
class Color:
    b: int
    g: int
    r: int

    @property
    def bgr(self):
        return self.b, self.g, self.r

    @property
    def rgb(self):
        return self.r, self.g, self.b
