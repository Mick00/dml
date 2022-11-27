from src.protocol.client.client import Client
from src.protocol.client.constants import CLIENT_MODULE
from src.protocol.states.state import State

ID_KEY = "id"
PEERS_KEY = "peers"
CLIENT_KEY = "client"
STARTED_KEY = "started"
IS_STOPPING_KEY = "is_stopping"
ROUND_KEY = "round"
RANK_KEY = "rank"


def get_client_state(state: State) -> dict:
    return state.get_module_state(CLIENT_MODULE)


def init_client(state: State, client):
    state.update_module(CLIENT_MODULE, {
        STARTED_KEY: True,
        CLIENT_KEY: client
    })


def set_is_stopping(state: State, is_stopping=True):
    state.update_module(CLIENT_MODULE, {
        IS_STOPPING_KEY: is_stopping,
    })


def get_client(state: State) -> Client:
    return get_client_state(state).get(CLIENT_KEY)


def get_node_id(state: State) -> str:
    return get_client_state(state).get(ID_KEY)


def client_is_started(state: State) -> bool:
    mod_state = get_client_state(state)
    return mod_state.get(STARTED_KEY, False)


def get_peers(state: State) -> set[str]:
    mod_state = get_client_state(state)
    return mod_state.get(PEERS_KEY, set())


def is_peer_registered(state: State, peer_id: str) -> bool:
    return peer_id in get_peers(state)


def add_peer(state: State, peer_id: str):
    peers = get_peers(state)
    peers.add(peer_id)
    state.update_module(CLIENT_MODULE, {PEERS_KEY: peers})


def get_round_id(state: State):
    return get_client_state(state).get(ROUND_KEY, -1)


def update_round_id(state: State, new_round_id: int):
    state.update_module(CLIENT_MODULE, {ROUND_KEY: new_round_id})


def get_node_rank(state: State) -> int:
    return state.get_module_state(CLIENT_MODULE).get(RANK_KEY)