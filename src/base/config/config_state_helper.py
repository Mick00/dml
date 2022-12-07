from src.base.config.constants import CONFIG_MODULE
from src.base.states.state import State


def get_config(state: State) -> dict:
    return state.get_module_state(CONFIG_MODULE)


def get_broker_host(state: State) -> (str, int):
    module_state = get_config(state)
    return module_state.get('broker_hostname'), module_state.get('broker_port')


def get_trainer_threshold(state: State) -> int:
    return get_config(state).get('trainer_threshold')


def get_local_model_name(state: State) -> str:
    return get_config(state).get('local_model')


def get_output_path(state: State) -> str:
    return get_config(state).get('training_out')


def gpu_enabled(state: State) -> bool:
    return get_config(state).get('enable_gpu', False)


def get_tracking_uri(state: State) -> str:
    return get_config(state).get('tracking_uri')


def get_experience_name(state: State) -> str:
    return get_config(state).get('experiment_name')