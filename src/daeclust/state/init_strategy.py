import os

from src.daeclust.constants import DAECLUST_MODULE
from src.daeclust.daecluste_helper import STRATEGY_KEY, get_strategy
from src.daeclust.strategy import AggregationStrategy
from src.base.client.client_state_helpers import get_node_id
from src.base.config.config_state_helper import get_output_path, get_local_model_name
from src.base.states.event import Event
from src.base.states.handler import Handler
from src.base.states.state import State
from src.base.states.transition import StateTransition
from src.base.training.events import StartRound


class InitStrategy(StateTransition):
    def transition(self, event: Event, state: State, handler: Handler):
        my_id = get_node_id(state)
        cache_path = os.path.join(get_output_path(state), "cache", my_id)
        default_local_model = get_local_model_name(state)
        state.update_module(DAECLUST_MODULE, {
            STRATEGY_KEY: AggregationStrategy(cache_path, default_local_model)
        })


class InitStrategyForRound(StateTransition):
    def transition(self, event: StartRound, state: State, handler: Handler):
        get_strategy(state).init_round(event.round_id)