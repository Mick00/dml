import unittest
import json

from src.protocol.client.messages.message import Message
from src.protocol.client.messages.serializer import Serializer


def message_factory(data=None):
    return Message("test_id", "test_type", 10, data)


class SerializerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.serializer = Serializer()

    def test_serialize_no_data(self):
        message = message_factory()
        serialized = self.serializer.serialize(message)
        self.assertTrue(isinstance(serialized, str))
        json_message = json.loads(serialized)
        self.assertEqual(json_message["from_id"], message.from_id)
        self.assertEqual(json_message["type"], message.type)
        self.assertEqual(json_message["round_id"], message.round_id)
        self.assertEqual(json_message["data"], {})

    def test_serialize_with_data(self):
        message = message_factory({"value": 123})
        serialized = self.serializer.serialize(message)
        json_message = json.loads(serialized)
        self.assertEqual(json_message["data"]["value"], 123)

    def test_deserialize_no_data(self):
        message = message_factory()
        serialized = self.serializer.serialize(message)
        deserialized = self.serializer.deserialize(serialized)
        self.assertEqual(deserialized.from_id, message.from_id)
        self.assertEqual(deserialized.type, message.type)
        self.assertEqual(deserialized.round_id, message.round_id)
        self.assertEqual(len(deserialized.data), 0)

    def test_deserialize_with_data(self):
        data = {"test": 123, "array": [1, 2, 3], "embed_dict": {"hello": "world"}}
        message = message_factory(data)
        serialized = self.serializer.serialize(message)
        deserialized = self.serializer.deserialize(serialized)
        self.assertEqual(deserialized.data.test, 123)
        self.assertEqual(deserialized.data.array, [1, 2, 3])
        self.assertEqual(deserialized.data.embed_dict.hello, "world")

    def test_avoid_leaking_data(self):
        data = {"test": 123}
        message = message_factory(data)
        message.foo = "bar"
        serialized = self.serializer.serialize(message)
        json_msg = json.loads(serialized)
        self.assertFalse("foo" in json_msg)


if __name__ == '__main__':
    unittest.main()