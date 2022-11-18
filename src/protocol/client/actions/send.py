from src.protocol.client.constants import CLIENT_SEND
from src.protocol.states.event import Event

class Send(Event):
    def __init__(self, event: Event):
        super(Send, self).__init__(CLIENT_SEND, event.__dict__)