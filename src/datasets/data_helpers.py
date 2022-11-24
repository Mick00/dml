from src.protocol.config.config_state_helper import get_config
from src.protocol.states.state import State


def get_data_path(state: State) -> str:
    return get_config(state).get('data_path')