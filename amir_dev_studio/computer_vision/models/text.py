from dataclasses import dataclass

from amir_dev_studio.computer_vision.models.base import Base
from amir_dev_studio.computer_vision.models.color import Color
from amir_dev_studio.computer_vision.models.configs import (
    get_default_render_thickness,
    get_default_render_font_scale,
    get_default_render_color
)
from amir_dev_studio.computer_vision.models.point import Point


@dataclass
class RenderableText(Base):
    value: str
    position: Point

    color: Color
    font_scale: float
    thickness: int

    def __copy__(self):
        return RenderableText(
            self.value,
            self.position,
            self.color,
            self.font_scale,
            self.thickness
        )

    @classmethod
    def from_string(
            cls,
            value: str,
            position: Point,
            color: Color = None,
            font_scale: float = None,
            thickness: int = None
    ):
        return cls(
            value,
            position,
            color or get_default_render_color(),
            font_scale or get_default_render_font_scale(),
            thickness or get_default_render_thickness()
        )
