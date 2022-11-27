from src.protocol.config.config_state_helper import get_config
from src.protocol.states.state import State

DATA_MODULE = "data"


def get_data_path(state: State) -> str:
    return get_config(state).get('data_path')


def get_dataset(state: State) -> str:
    return get_config(state).get('dataset')


def get_lower_bound(state: State) -> str:
    return get_config(state).get('lower_bound')


def get_higher_bound(state: State) -> str:
    return get_config(state).get('higher_bound')


def get_data_module(state: State) -> dict:
    return state.get_module_state(DATA_MODULE)

