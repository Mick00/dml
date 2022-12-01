from src.base.client.client_state_helpers import get_peers, get_node_id, RANK_KEY
from src.base.client.constants import CLIENT_MODULE
from src.base.states.event import Event
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandler


class SetClientRank(EventHandler):

    def transition(self, event: Event, state: State, handler: EventListener):
        my_id = get_node_id(state)
        peers = (list(get_peers(state)) + [my_id])
        peers.sort()
        rank = peers.index(my_id)
        state.update_module(CLIENT_MODULE, {
            RANK_KEY: rank
        })