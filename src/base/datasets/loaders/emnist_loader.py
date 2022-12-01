from torchvision import datasets
from torchvision.transforms import ToTensor

from src.base.datasets.data_helpers import get_data_path
from src.base.datasets.data_loader import get_data_loader
from src.base.states.event import Event
from src.base.states.handler import Handler
from src.base.states.state import State
from src.base.states.transition import StateTransition


class EmnistRegister(StateTransition):
    def transition(self, event: Event, state: State, handler: Handler):
        data_loader = get_data_loader(state)
        data_path = get_data_path(state)
        data_loader.register_loader("emnist", lambda state: load_emnist(data_path))


def load_emnist(data_path: str):
    return datasets.EMNIST(
        data_path,
        split="bymerge",
        train=True,
        download=True,
        transform=ToTensor()
    ), datasets.EMNIST(
        data_path,
        split="bymerge",
        train=False,
        download=True,
        transform=ToTensor()
    )
