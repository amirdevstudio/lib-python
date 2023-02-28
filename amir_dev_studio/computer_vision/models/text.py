from dataclasses import dataclass

from amir_dev_studio.computer_vision.models.base import RenderableShape
from amir_dev_studio.computer_vision.models.color import Color
from amir_dev_studio.computer_vision.models.point import Point


@dataclass
class Text(str, RenderableShape):
    @property
    def position(self) -> Point:
        return self.render_args.get('position')

    @position.setter
    def position(self, value: Point):
        self.render_args['position'] = value

    @property
    def color(self) -> Color:
        return self.render_args.get('color')

    @color.setter
    def color(self, value: Color):
        self.render_args['color'] = value

    @property
    def font_scale(self) -> float:
        return self.render_args.get('font_scale')

    @font_scale.setter
    def font_scale(self, value: float):
        self.render_args['font_scale'] = value

    @property
    def thickness(self) -> int:
        return self.render_args.get('thickness')
