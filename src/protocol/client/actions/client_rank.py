from src.protocol.client.client_state_helpers import get_peers, get_node_id, RANK_KEY
from src.protocol.client.constants import CLIENT_MODULE
from src.protocol.states.event import Event
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition


class SetClientRank(StateTransition):

    def transition(self, event: Event, state: State, handler: Handler):
        my_id = get_node_id(state)
        peers = (list(get_peers(state)) + [my_id])
        peers.sort()
        rank = peers.index(my_id)
        state.update_module(CLIENT_MODULE, {
            RANK_KEY: rank
        })