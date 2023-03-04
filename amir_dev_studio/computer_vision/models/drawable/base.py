from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from amir_dev_studio.computer_vision.models.base import Base

_T = TypeVar('_T')


class Drawable(Base, ABC, Generic[_T]):
    @abstractmethod
    def draw(self, pixels: _T) -> _T:
        pass
