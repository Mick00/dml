from src.base.client.client_state_helpers import get_peers, get_node_id, RANK_KEY
from src.base.client.constants import CLIENT_MODULE
from src.base.states.event import Event
from src.base.states.handler import Handler
from src.base.states.state import State
from src.base.states.transition import StateTransition


class SetClientRank(StateTransition):

    def transition(self, event: Event, state: State, handler: Handler):
        my_id = get_node_id(state)
        peers = (list(get_peers(state)) + [my_id])
        peers.sort()
        rank = peers.index(my_id)
        state.update_module(CLIENT_MODULE, {
            RANK_KEY: rank
        })