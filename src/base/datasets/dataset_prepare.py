from src.base.datasets.data_loader import get_data_loader
from src.base.states.event import Event
from src.base.states.handler import Handler
from src.base.states.state import State
from src.base.states.transition import StateTransition


class DatasetPrepare(StateTransition):
    def transition(self, event: Event, state: State, handler: Handler):
        data_loader = get_data_loader(state)
        data_loader.load_data(state)

