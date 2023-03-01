from unittest import TestCase

from amir_dev_studio.computer_vision.constants import Colors
from amir_dev_studio.computer_vision.models.image import Image
from amir_dev_studio.computer_vision.models.point import Point
from amir_dev_studio.computer_vision.models.rectangle import RenderableRectangle
from amir_dev_studio.computer_vision.models.text import RenderableText as Text


class TestImageCase(TestCase):
    def test_draw_rectangle_mutator(self):
        image = Image.create_blank(100, 100)

        rect = RenderableRectangle(Point(10, 10), Point(20, 20), Colors.RED, 1)
        image.add_rectangle(rect)

        rect = RenderableRectangle(Point(30, 30), Point(40, 40), Colors.GREEN, 1)
        image.add_rectangle(rect)

        image.render_rectangles()
        image.show()

    def test_apply_brightness(self):
        image = Image.create_blank(100, 100)
        image = image.apply_brightness(100)
        image.show()

    def test_add_text(self):
        image = Image.create_blank(400, 400)
        text = Text.from_string('Hello World', Point(40, 40), Colors.RED, 1, 1)
        image.add_text(text)
        image.render_texts()
        image.show()

    def test_copy_image(self):
        image = Image.create_blank(100, 100)
        image.add_rectangle(RenderableRectangle(Point(10, 10), Point(20, 20), Colors.RED, 1))
        image.add_rectangle(RenderableRectangle(Point(30, 30), Point(40, 40), Colors.GREEN, 1))

        image_copy = image.copy()

        assert len(image_copy.rectangles) == 2
        assert len(image.rectangles) == 2
