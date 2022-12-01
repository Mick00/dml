from src.nsclust.events import SelectedUpdates
from src.nsclust.start_selection import StartUpdateSelection
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandler
from src.base.training.fedml.fedml_state_helper import get_update_queue


class AcceptAllUpdates(EventHandler):

    def transition(self, event: StartUpdateSelection, state: State, handler: EventListener):
        update_queue = get_update_queue(state).get_queue(event.round_id)
        handler.queue_event(SelectedUpdates(event.round_id, update_queue))
