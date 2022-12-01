from src.daeclust.daecluste_helper import get_strategy
from src.daeclust.state.events import UpdatePooled, StartUpdateSelection
from src.base.client.client_state_helpers import get_peers
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandler


class TriggerUpdateSelection(EventHandler):
    def transition(self, event: UpdatePooled, state: State, handler: EventListener):
        round_id = event.update.round_id
        round_strategy = get_strategy(state).for_round(round_id)
        if round_strategy.update_pools.total_updates == len(get_peers(state))+1:
            handler.queue_event(StartUpdateSelection(round_id))