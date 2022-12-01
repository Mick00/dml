from src.base.datasets.data_loader import get_data_loader
from src.base.datasets.sampling_rules.balance import balanced_weight
from src.base.states.event import Event
from src.base.states.state import State
from src.base.states.event_handler import EventHandlerSimple, Handler


class ConfigureBalancedSampler(EventHandlerSimple):
    def transition(self, event: Event, state: State, handler: Handler):
        data_loader = get_data_loader(state)
        data_loader.set_sampling_rules([balanced_weight()])