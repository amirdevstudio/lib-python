from amir_dev_studio.events.broker import EventBroker
from amir_dev_studio.events.event import Event

broker = EventBroker()
broker.add_subscriber('test', print)
broker.publish(Event('test'))

