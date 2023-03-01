from unittest import TestCase

from amir_dev_studio.computer_vision.constants import Colors
from amir_dev_studio.computer_vision.models.image import Image
from amir_dev_studio.computer_vision.models.point import Point
from amir_dev_studio.computer_vision.models.renderable.rectangle import Rectangle
from amir_dev_studio.computer_vision.models.renderable.text import Text


class TestImageCase(TestCase):
    def test_draw_rectangle_functional(self):
        image = Image.create_blank(100, 100)

        rect = Rectangle(Point(10, 10), Point(20, 20))
        rect.color = Colors.RED
        image = image.add_rectangle(rect)

        rect = Rectangle(Point(30, 30), Point(40, 40))
        rect.color = Colors.GREEN
        image = image.add_rectangle(rect)

        image = image.render_rectangles()
        image.show()

    def test_draw_rectangle_mutator(self):
        image = Image.create_blank(100, 100)

        rect = Rectangle(Point(10, 10), Point(20, 20))
        rect.color = Colors.RED
        image.add_rectangle_(rect)

        rect = Rectangle(Point(30, 30), Point(40, 40))
        rect.color = Colors.GREEN
        image.add_rectangle_(rect)

        image.render_rectangles_()
        image.show()

    def test_apply_brightness(self):
        image = Image.create_blank(100, 100)
        image = image.apply_brightness_(100)
        image.show()

    def test_add_text(self):
        image = Image.create_blank(400, 400)
        text = Text('Hello World')
        text.position = Point(40, 40)
        text.color = Colors.RED
        text.font_scale = 1
        text.thickness = 1
        image.add_text_(text)
        image.render_texts_()
        image.show()
