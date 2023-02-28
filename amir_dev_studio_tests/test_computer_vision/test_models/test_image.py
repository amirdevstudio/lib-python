from unittest import TestCase

from amir_dev_studio.computer_vision.constants import Colors
from amir_dev_studio.computer_vision.models.image import Image
from amir_dev_studio.computer_vision.models.point import Point
from amir_dev_studio.computer_vision.models.rectangle import Rectangle


class TestImageCase(TestCase):
    def test_draw_rectangle_functional(self):
        image = Image.create_blank(100, 100)
        image = image.draw_rectangle(Rectangle(Point(10, 10), Point(20, 20)), Colors.RED)
        image = image.draw_rectangle(Rectangle(Point(30, 30), Point(40, 40)), Colors.GREEN)
        image = image.render_rectangles()
        image.show()

    def test_draw_rectangle_mutator(self):
        image = Image.create_blank(100, 100)
        image.draw_rectangle_(Rectangle(Point(10, 10), Point(20, 20)), Colors.RED)
        image.draw_rectangle_(Rectangle(Point(30, 30), Point(40, 40)), Colors.GREEN)
        image.render_rectangles_()
        image.show()

    def test_apply_brightness(self):
        image = Image.create_blank(100, 100)
        image = image.apply_brightness_(100)
        image.show()