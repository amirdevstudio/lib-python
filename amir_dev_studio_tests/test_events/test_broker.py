from amir_dev_studio.events import EventBroker

broker = EventBroker()
broker.add_subscriber('test', print)
broker.add_publisher(...)
