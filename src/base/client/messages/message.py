from src.base.states.event_listener import Event


def wrap_event(from_id: str, round_id: int, event: Event):
    msg = Message(from_id, event.type, round_id)
    msg.data = event.data
    return msg


class Message(Event):
    def __init__(self, from_id: str, e_type: str, round_id: int, data_dict=None):
        super().__init__(e_type, data_dict)
        self.from_id = from_id
        self.round_id = round_id
