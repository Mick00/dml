from src.nsclust.events import SelectedUpdates
from src.nsclust.start_selection import StartUpdateSelection
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition
from src.protocol.training.fedml.fedml_state_helper import get_update_queue


class AcceptAllUpdates(StateTransition):

    def transition(self, event: StartUpdateSelection, state: State, handler: Handler):
        update_queue = get_update_queue(state).get_queue(event.round_id)
        handler.queue_event(SelectedUpdates(event.round_id, update_queue))
