import unittest

from src.base.states.event import Event
from src.base.client.messages.message import Message, wrap_event, load_message
from src.base.client.messages.serializer import Serializer


class MessageTest(unittest.TestCase):

    def test_event_type(self):
        from_id = 'user0'
        type = "test"
        round = 99
        msg = Message(from_id, type, round)
        self.assertEqual(msg.type, type)
        self.assertEqual(msg.data, None)
        self.assertEqual(msg.has_data(), False)
        self.assertEqual(msg.from_id, from_id)
        self.assertEqual(msg.round_id, round)

    def test_event_data(self):
        from_id = 'user0'
        type = "test"
        round = 99
        msg = Message(from_id, type, round, {
            "hello": "world",
            "array": [1, 2, 3],
            "sub": {"new": "world", "test": "yes"}
        })
        self.assertEqual(msg.type, type)
        self.assertEqual(msg.has_data(), True)
        self.assertEqual(msg.data.hello, "world")
        self.assertEqual(msg.data.array, [1, 2, 3])
        self.assertEqual(msg.data.sub.new, "world")
        self.assertEqual(msg.data.sub.test, "yes")
        self.assertEqual(msg.from_id, from_id)
        self.assertEqual(msg.round_id, round)

    def test_wrap_event(self):
        from_id = 'user0'
        type = "test"
        round = 99
        e = Event(type, {"hello": "world"})
        msg = wrap_event(from_id, round, e)
        self.assertEqual(msg.type, type)
        self.assertEqual(msg.data.hello, "world")
        self.assertEqual(msg.has_data(), True)
        self.assertEqual(msg.from_id, from_id)
        self.assertEqual(msg.round_id, round)


if __name__ == '__main__':
    unittest.main()