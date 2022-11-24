from src.datasets.data_helpers import get_data_path
from src.datasets.mnist.mnist_loader import load_mnist
from src.protocol.states.event import Event
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition
from src.protocol.training.training_state_helper import get_training_client


class TrainingClientDataLoader(StateTransition):
    def transition(self, event: Event, state: State, handler: Handler):
        data_path = get_data_path(state)
        train_dataset, test_dataset = load_mnist(data_path)
        training_client = get_training_client(state)
        training_client.set_dataset(train_dataset, test_dataset)