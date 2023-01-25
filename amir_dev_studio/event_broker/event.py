from dataclasses import dataclass

from amir_dev_studio.event_broker.base import AbstractEvent


@dataclass(frozen=True)
class Event(AbstractEvent):
    name: str
