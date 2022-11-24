from src.daeclust.daecluste_helper import get_strategy
from src.daeclust.state.events import UpdatePooled, StartUpdateSelection
from src.protocol.client.client_state_helpers import get_peers
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition


class TriggerUpdateSelection(StateTransition):
    def transition(self, event: UpdatePooled, state: State, handler: Handler):
        round_id = event.update.round_id
        round_strategy = get_strategy(state).for_round(round_id)
        if round_strategy.update_pools.total_updates == len(get_peers(state))+1:
            handler.queue_event(StartUpdateSelection(round_id))