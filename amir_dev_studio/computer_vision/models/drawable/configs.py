from amir_dev_studio.computer_vision.constants import Colors
from amir_dev_studio.computer_vision.models.color import Color

default_render_color: Color = Colors.RED
default_render_font_scale: float = 1.0
default_render_thickness: int = 1


def get_default_color() -> Color:
    return default_render_color


def set_default_color(color: Color):
    global default_render_color
    default_render_color = color


def get_default_render_thickness() -> int:
    return default_render_thickness


def set_default_render_thickness(thickness: int):
    global default_render_thickness
    default_render_thickness = thickness


def get_default_render_font_scale() -> float:
    return default_render_font_scale


def set_default_render_font_scale(font_scale: float):
    global default_render_font_scale
    default_render_font_scale = font_scale
