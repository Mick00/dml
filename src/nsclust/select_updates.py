from src.nsclust.events import SelectedUpdates
from src.nsclust.start_selection import StartUpdateSelection
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandler
from src.base.training.constants import TRAINING_MODULE
from src.base.training.fedml.fedml_state_helper import get_update_queue


class AcceptAllUpdates(EventHandler):

    def transition(self, event: StartUpdateSelection, state: State, handler: EventListener):
        update_queue = get_update_queue(state).get_queue(event.round_id)
        handler.queue_event(SelectedUpdates(event.round_id, update_queue))


class SelectUpdatesCleanup(EventHandler):
    def transition(self, event: SelectedUpdates, state: State, handler: EventListener):
        state.update_module(TRAINING_MODULE, {
            "test_thread": None
        })