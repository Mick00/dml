from src.base.client.client_state_helpers import get_peers
from src.base.states.event import Event
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandler
from src.nsclust.constants import START_SELECTION
from src.base.training.fedml.update_queue import QueuedUpdate


class StartUpdateSelection(Event):
    def __init__(self, round_id: int):
        super().__init__(START_SELECTION)
        self.round_id = round_id


class StartUpdateSelectionTransition(EventHandler):
    def transition(self, event: QueuedUpdate, state: State, handler: EventListener):
        if len(event.queue) >= len(get_peers(state)) + 1:
            handler.queue_event(StartUpdateSelection(event.update.round_id))