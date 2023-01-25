from amir_dev_studio.event_broker import EventBroker

broker = EventBroker()
broker.add_subscriber('test', print)
broker.add_publisher(...)
