from unittest import TestCase

from amir_dev_studio.computer_vision.models.drawable.text import Text


class TestText(TestCase):
    def test_text(self):
        text = Text('Hello World')
        assert isinstance(text, str)
        assert text == 'Hello World'
