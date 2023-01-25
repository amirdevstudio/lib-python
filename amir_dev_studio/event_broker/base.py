from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class AbstractEvent(ABC):
    ...


class AbstractSubscriber(ABC):
    def __init__(self):
        self.await_handle = False

    @abstractmethod
    def handle(self, event: AbstractEvent):
        ...


class AbstractEventBroker(ABC):
    def __init__(self):
        self.subscribers = {}

    @abstractmethod
    def add_subscriber(self, event_name: str, subscriber: AbstractSubscriber | Callable[[AbstractEvent], None]):
        ...

    @abstractmethod
    def publish(self, event: AbstractEvent):
        ...
