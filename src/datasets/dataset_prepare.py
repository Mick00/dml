from src.datasets.data_loader import get_data_loader
from src.protocol.states.event import Event
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition
from src.protocol.training.training_state_helper import get_training_client


class DatasetPrepare(StateTransition):
    def transition(self, event: Event, state: State, handler: Handler):
        data_loader = get_data_loader(state)
        train_dataset, val_dataset, test_dataset = data_loader.load_data(state)
        training_client = get_training_client(state)
        training_client.set_dataset(train_dataset, val_dataset, test_dataset)

