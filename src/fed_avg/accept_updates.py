from src.nsclust.events import SelectedUpdates
from src.nsclust.start_selection import StartUpdateSelection
from src.base.states.handler import Handler
from src.base.states.state import State
from src.base.states.transition import StateTransition
from src.base.training.fedml.fedml_state_helper import get_update_queue


class AcceptAllUpdates(StateTransition):

    def transition(self, event: StartUpdateSelection, state: State, handler: Handler):
        update_queue = get_update_queue(state).get_queue(event.round_id)
        handler.queue_event(SelectedUpdates(event.round_id, update_queue))
