from src.base.datasets.data_loader import get_data_loader
from src.base.states.event import Event
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandler
from src.base.training.training_state_helper import get_training_client


class DatasetPrepare(EventHandler):
    def _transition(self, event: Event, state: State, handler: EventListener):
        data_loader = get_data_loader(state)
        loaded_dataset = data_loader.load_data(state)
        get_training_client(state).add_tag("dataset", loaded_dataset)
        return [self.log_info(event.type, {"dataset": loaded_dataset})]

