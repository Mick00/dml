import json

from src.base.client.client_state_helpers import get_node_rank
from src.base.config.config_state_helper import get_config
from src.daeclust.constants import DAECLUST_MODULE
from src.daeclust.strategy import AggregationStrategy
from src.base.states.state import State


STRATEGY_KEY = "strategy"


def get_daeclust_state_module(state: State):
    return state.get_module_state(DAECLUST_MODULE)


def get_strategy(state: State) -> AggregationStrategy:
    return get_daeclust_state_module(state).get(STRATEGY_KEY)


def get_div_tolerance(state: State) -> float:
    value = get_config(state).get("divergence_tolerance", "3.0")
    if value.isnumeric() or value[1:].isnumeric():
        return int(value)
    values = json.loads(value)
    value = values[get_node_rank(state) % len(values)]
    if not isinstance(value, int):
        value = int(value)
    return value


def get_cluster_metric(state: State) -> str:
    return get_config(state).get('cluster_metric')


def get_cluster_scoring(state: State) -> str:
    return get_config(state).get('cluster_scoring')


def get_divergence_method(state: State) -> str:
    return get_config(state).get("divergence_method")
