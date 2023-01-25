from amir_dev_studio.events.base import AbstractEventBroker
from amir_dev_studio.events.event import Event


class EventBroker(AbstractEventBroker):
    def add_subscriber(self, event_name, subscriber):
        self.subscribers.setdefault(event_name, [])
        self.subscribers[event_name].append(subscriber)

    def publish(self, event: Event):
        for subscriber in self.subscribers.get(event.name, []):
            subscriber.handle(event)
