from src.daeclust.start_selection import StartUpdateSelection
from src.protocol.client.client_state_helpers import get_peers
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition
from src.protocol.training.fedml.update_queue import QueuedUpdate


class FedAvgStartAgg(StateTransition):
    def transition(self, event: QueuedUpdate, state: State, handler: Handler):
        if event.update.round_id == 0:
            handler.queue_event(StartUpdateSelection(event.update.round_id))
        elif len(event.queue) >= len(get_peers(state)) + 1:
            handler.queue_event(StartUpdateSelection(event.update.round_id))