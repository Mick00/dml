from src.daeclust.state.events import UpdatesPooled, StartUpdateSelection
from src.base.client.client_state_helpers import get_peers
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandlerSimple


class TriggerUpdateSelection(EventHandlerSimple):
    def transition(self, event: UpdatesPooled, state: State, handler: EventListener):
        round_id = event.round_id
        if event.trainers_entered == len(get_peers(state))+1:
            handler.queue_event(StartUpdateSelection(round_id))
