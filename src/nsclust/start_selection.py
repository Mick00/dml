from src.base.client.client_state_helpers import get_peers
from src.base.states.event import Event
from src.base.states.handler import Handler
from src.base.states.state import State
from src.base.states.transition import StateTransition
from src.nsclust.constants import START_SELECTION
from src.base.training.fedml.update_queue import QueuedUpdate


class StartUpdateSelection(Event):
    def __init__(self, round_id: int):
        super().__init__(START_SELECTION)
        self.round_id = round_id


class StartUpdateSelectionTransition(StateTransition):
    def transition(self, event: QueuedUpdate, state: State, handler: Handler):
        if len(event.queue) >= len(get_peers(state)) + 1:
            handler.queue_event(StartUpdateSelection(event.update.round_id))