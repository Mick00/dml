from src.protocol.states.handler import Event


def event_factory(type: str, data: dict):
    return Event(type, data)