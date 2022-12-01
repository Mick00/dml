from src.base.client.actions.constants import NEW_PEER
from src.base.states.event import Event


class NewPeer(Event):
    def __init__(self, registered_id: str):
        super(NewPeer, self).__init__(
            NEW_PEER
        )
        self.data.registered_id = registered_id
