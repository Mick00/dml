from src.datasets.data_loader import get_data_loader
from src.datasets.sampling_rules.balance import balanced_weight
from src.protocol.states.event import Event
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition, Handler


class ConfigureDataset(StateTransition):
    def transition(self, event: Event, state: State, handler: Handler):
        data_loader = get_data_loader(state)
        data_loader.set_sampling_rules([balanced_weight()])