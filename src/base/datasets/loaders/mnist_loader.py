
from torchvision.datasets import MNIST
from torchvision.transforms import transforms

from src.base.datasets.data_helpers import get_data_path
from src.base.datasets.data_loader import get_data_loader
from src.base.states.event import Event
from src.base.states.state import State
from src.base.states.transition import Handler, StateTransition


class MnistRegister(StateTransition):
    def transition(self, event: Event, state: State, handler: Handler):
        data_loader = get_data_loader(state)
        data_path = get_data_path(state)
        data_loader.register_loader("mnist", lambda state: load_mnist(data_path))


def load_mnist(data_path: str):
    train_dataset = MNIST(
        data_path,
        train=True,
        download=True,
        transform=transforms.ToTensor()
    )
    test_dataset = MNIST(
        data_path,
        train=False,
        download=True,
        transform=transforms.ToTensor()
    )
    return train_dataset, test_dataset
