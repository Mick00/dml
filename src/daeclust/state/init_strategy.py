import os

from src.daeclust.constants import DAECLUST_MODULE
from src.daeclust.daecluste_helper import STRATEGY_KEY, get_strategy
from src.daeclust.strategy import AggregationStrategy
from src.base.client.client_state_helpers import get_node_id
from src.base.config.config_state_helper import get_output_path, get_local_model_name
from src.base.states.event import Event
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandler
from src.base.training.events import StartRound


class InitStrategy(EventHandler):
    def transition(self, event: Event, state: State, handler: EventListener):
        my_id = get_node_id(state)
        cache_path = os.path.join(get_output_path(state), "cache", my_id)
        default_local_model = get_local_model_name(state)
        state.update_module(DAECLUST_MODULE, {
            STRATEGY_KEY: AggregationStrategy(cache_path, default_local_model)
        })


class InitStrategyForRound(EventHandler):
    def transition(self, event: StartRound, state: State, handler: EventListener):
        get_strategy(state).init_round(event.round_id)