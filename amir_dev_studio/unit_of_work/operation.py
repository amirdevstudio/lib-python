from abc import abstractmethod, ABC


class AbstractOperation(ABC):
    def __init__(self):
        self.was_successful = False
        self.exception = None

    @abstractmethod
    def execute(self, *args, **kwargs):
        ...
