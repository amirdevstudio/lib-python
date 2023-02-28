from abc import ABC
from unittest import TestCase

from amir_dev_studio.dependency_injection.providers import Singleton, Transient


class TestDecorators(TestCase):
    def test_register_transient(self):

        class AbstractFoo(ABC):
            pass

        class Foo(AbstractFoo):
            pass


class TestTransient(TestCase):
    ...
