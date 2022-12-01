from src.nsclust.start_selection import StartUpdateSelection
from src.base.client.client_state_helpers import get_peers
from src.base.states.handler import Handler
from src.base.states.state import State
from src.base.states.transition import StateTransition
from src.base.training.fedml.update_queue import QueuedUpdate


class FedAvgStartAgg(StateTransition):
    def transition(self, event: QueuedUpdate, state: State, handler: Handler):
        if event.update.round_id == 0:
            handler.queue_event(StartUpdateSelection(event.update.round_id))
        elif len(event.queue) >= len(get_peers(state)) + 1:
            handler.queue_event(StartUpdateSelection(event.update.round_id))