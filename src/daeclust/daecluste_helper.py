from src.daeclust.constants import DAECLUST_MODULE
from src.daeclust.strategy import AggregationStrategy
from src.base.states.state import State


STRATEGY_KEY = "strategy"


def get_daeclust_state_module(state: State):
    return state.get_module_state(DAECLUST_MODULE)


def get_strategy(state: State) -> AggregationStrategy:
    return get_daeclust_state_module(state).get(STRATEGY_KEY)
