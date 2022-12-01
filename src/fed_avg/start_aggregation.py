from src.base.datasets.data_helpers import data_is_ready
from src.nsclust.start_selection import StartUpdateSelection
from src.base.client.client_state_helpers import get_peers
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandlerSimple
from src.base.training.fedml.update_queue import QueuedUpdate


class FedAvgStartAgg(EventHandlerSimple):
    def transition(self, event: QueuedUpdate, state: State, handler: EventListener):
        if event.update.round_id == 0:
            if data_is_ready(state):
                handler.queue_event(StartUpdateSelection(event.update.round_id))
            else:
                handler.queue_event(event)
        elif len(event.queue) >= len(get_peers(state)) + 1:
            handler.queue_event(StartUpdateSelection(event.update.round_id))