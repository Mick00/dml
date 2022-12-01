from src.base.datasets.data_loader import get_data_loader
from src.base.states.event import Event
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandler


class DatasetPrepare(EventHandler):
    def transition(self, event: Event, state: State, handler: EventListener):
        data_loader = get_data_loader(state)
        data_loader.load_data(state)

