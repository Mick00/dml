import json

from .message import Message


def load_message(message: dict):
    return Message(message["from_id"], message["type"], message["round_id"], message["data"])


# Avoids sharing data that could be stored at the base message
def clean_message(message: Message):
    return {
        "from_id": message.from_id,
        "type": message.type,
        "round_id": message.round_id,
        "data": message.data
    }


class JSONSerializer(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


class Serializer:
    def serialize(self, message: Message):
        return json.dumps(clean_message(message), cls=JSONSerializer)

    def deserialize(self, message: str) -> Message:
        json_message = json.loads(message)
        return load_message(json_message)
