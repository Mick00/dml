from src.protocol.client.client_state_helpers import get_peers
from src.protocol.states.event import Event
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition
from src.nsclust.constants import START_SELECTION
from src.protocol.training.fedml.update_queue import QueuedUpdate


class StartUpdateSelection(Event):
    def __init__(self, round_id: int):
        super().__init__(START_SELECTION)
        self.round_id = round_id


class StartUpdateSelectionTransition(StateTransition):
    def transition(self, event: QueuedUpdate, state: State, handler: Handler):
        if len(event.queue) >= len(get_peers(state)) + 1:
            handler.queue_event(StartUpdateSelection(event.update.round_id))