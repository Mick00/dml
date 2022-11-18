import unittest

from src.protocol.client.messages.message import Message
from src.protocol.states.state import State
from src.protocol.states.handler import Handler, StateTransition


def message_factory(from_id="test_id", type="test_type", round_id=10, data=None):
    return Message(from_id, type, round_id, data)


class FakeReducer(StateTransition):

    def __init__(self, key, value, priority=100):
        super().__init__(priority)
        self.key = key
        self.value = value

    def transition(self, message: Message, state: State, handler: Handler):
        state.update_module("test", {self.key: self.value, "foo": message.data.foo})


class SerializerTest(unittest.TestCase):

    def test_get_no_reducers(self):
        handler = Handler()
        reducers = handler.get_reducers("test_type")
        self.assertEqual(reducers, [])

    def test_get_reducers(self):
        handler = Handler()
        type = "foo"
        reducer0 = FakeReducer("hello", "world", 50)
        reducer1 = FakeReducer("how", "are you?", 100)
        reducer2 = FakeReducer("test", "bar", 75)
        handler.register_reducer(type, reducer0)
        handler.register_reducer(type, reducer1)
        handler.register_reducer(type, reducer2)
        self.assertEqual(handler.get_reducers(type), [reducer0, reducer2, reducer1])

    def test_queue_event(self):
        handler = Handler()
        event = message_factory()
        handler.queue_event(event)
        self.assertEqual(handler.event_queue.get(), event)

    def test_register_handler(self):
        handler = Handler()
        type = "foo"
        reducer0 = FakeReducer("hello", "world", 50)
        reducer1 = FakeReducer("how", "are you?", 100)
        reducer2 = FakeReducer("test", "bar", 75)
        handler.register_reducer(type, reducer0)
        handler.register_reducer(type, reducer1)
        handler.register_reducer(type, reducer2)
        reducers = handler.reducers[type]
        self.assertEqual(reducers[0], reducer0)
        self.assertEqual(reducers[1], reducer2)
        self.assertEqual(reducers[2], reducer1)

    def test_handle_event(self):
        handler = Handler()
        type = "foo"
        reducer0 = FakeReducer("hello", "world", 50)
        reducer1 = FakeReducer("how", "are you?", 100)
        reducer2 = FakeReducer("hello", "bar", 75)
        handler.register_reducer(type, reducer0)
        handler.register_reducer(type, reducer1)
        handler.register_reducer(type, reducer2)
        message = message_factory("boo_id", type, 10, {"foo": "fuze"})
        handler.handle_event(message)
        self.assertEqual(handler.state.get_module_state("test")["hello"], "bar")
        self.assertEqual(handler.state.get_module_state("test")["how"], "are you?")
        self.assertEqual(handler.state.get_module_state("test")["foo"], "fuze")


if __name__ == '__main__':
    unittest.main()
