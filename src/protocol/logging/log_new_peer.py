from src.protocol.client.actions.new_peer import NewPeer
from src.protocol.client.client_state_helpers import get_peers
from src.protocol.logging.logger import get_logger
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition


class LogNewPeer(StateTransition):
    def transition(self, event: NewPeer, state: State, handler: Handler):
        peer_count = len(get_peers(state))
        get_logger(state).info(event.type, extra={"peer_id": event.data.registered_id, "peer_count": peer_count})