from abc import abstractmethod, ABC
from dataclasses import dataclass, field


@dataclass
class Base(ABC):
    extra_data: dict = field(
        init=False,
        default_factory=dict,
        repr=False
    )

    @abstractmethod
    def __copy__(self):
        pass

    def copy(self):
        return self.__copy__()
