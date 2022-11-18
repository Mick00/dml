from src.protocol.client.messages.message import Message


def message_factory(from_id="test_id", type="test_type", round_id=10, data=None):
    return Message(from_id, type, round_id, data)
