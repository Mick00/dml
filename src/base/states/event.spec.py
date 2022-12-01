import unittest
from src.base.states.event import Event


class EventTest(unittest.TestCase):
    def test_event_type(self):
        type = "test"
        e = Event(type)
        self.assertEqual(e.type, type)
        self.assertEqual(len(e.data), 0)
        self.assertEqual(e.has_data(), False)

    def test_event_data(self):
        type = "test"
        e = Event(type, {
            "hello": "world",
            "array": [1, 2, 3],
            "sub": {"new": "world", "test": "yes"}
        })
        self.assertEqual(e.type, type)
        self.assertEqual(e.has_data(), True)
        self.assertEqual(e.data.hello, "world")
        self.assertEqual(e.data.array, [1, 2, 3])
        self.assertEqual(e.data.sub.new, "world")
        self.assertEqual(e.data.sub.test, "yes")


if __name__ == '__main__':
    unittest.main()