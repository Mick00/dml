from src.base.client.actions.new_peer import NewPeer
from src.base.client.client_state_helpers import get_peers
from src.base.logging.logging_helpers import get_logger
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandler


class LogNewPeer(EventHandler):
    def transition(self, event: NewPeer, state: State, handler: EventListener):
        peer_count = len(get_peers(state))
        get_logger(state).info(event.type, extra={"peer_id": event.data.registered_id, "peer_count": peer_count})