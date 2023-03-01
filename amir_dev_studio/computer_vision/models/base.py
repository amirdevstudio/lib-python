from abc import abstractmethod, ABC
from dataclasses import dataclass, field


@dataclass
class Model(ABC):
    extra_data: dict = field(init=False, default_factory=dict, repr=False)

    def copy(self, *, __copy_method='__copy__'):
        assert hasattr(self, __copy_method), f'Class must implement {__copy_method} method to be copyable'
        return getattr(self, __copy_method)()
