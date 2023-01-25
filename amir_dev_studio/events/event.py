from dataclasses import dataclass

from amir_dev_studio.events.base import AbstractEvent


@dataclass(frozen=True)
class Event(AbstractEvent):
    name: str
