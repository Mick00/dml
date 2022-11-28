from src.protocol.client.client_state_helpers import get_peers, get_node_rank
from src.protocol.config.config_state_helper import get_config
from src.protocol.states.state import State

DATA_MODULE = "data"


def get_data_path(state: State) -> str:
    return get_config(state).get('data_path')


def get_dataset(state: State) -> str:
    return get_config(state).get('dataset')


def apply_balance_rule(state: State) -> bool:
    return get_config(state).get('data_balance')


def apply_partitions_rule(state: State) -> bool:
    return get_config(state).get('data_n_partitions') >= 0


def data_n_partitions(state: State) -> int:
    n_partitions = get_config(state).get('data_n_partitions')
    if n_partitions == 0:
        n_partitions = len(get_peers(state)) + 1
    return n_partitions


def data_partition_index(state: State) -> int:
    i_partition = get_config(state).get('data_partition_index')
    if i_partition == -1:
        i_partition = get_node_rank(state)
    return i_partition


def apply_target_bounds(state: State) -> bool:
    return get_lower_bound(state) >= 0 and get_higher_bound(state) >= 0


def get_lower_bound(state: State) -> int:
    return get_config(state).get('data_lower_bound')


def get_higher_bound(state: State) -> int:
    return get_config(state).get('data_higher_bound')


def apply_normal_probability(state: State) -> bool:
    return get_distribution_mean(state) >= 0 and get_distribution_std(state) >= 0


def get_distribution_mean(state: State) -> int:
    return get_config(state).get('data_mean')


def get_distribution_std(state: State) -> int:
    return get_config(state).get('data_std')


def get_data_module(state: State) -> dict:
    return state.get_module_state(DATA_MODULE)

