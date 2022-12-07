from torchvision import datasets
from torchvision.transforms import ToTensor

from src.base.datasets.data_helpers import get_data_path
from src.base.datasets.data_loader import get_data_loader
from src.base.states.event import Event
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandlerSimple


class FmnistRegister(EventHandlerSimple):
    def transition(self, event: Event, state: State, handler: EventListener):
        data_loader = get_data_loader(state)
        data_loader.register_loader("fmnist", lambda state: load_fmnist(get_data_path(state)))


def load_fmnist(data_path: str):
    if not data_path:
        raise Exception("data_path is not set")
    return datasets.FashionMNIST(
        data_path,
        train=True,
        download=True,
        transform=ToTensor()
    ), datasets.FashionMNIST(
        data_path,
        train=False,
        download=True,
        transform=ToTensor()
    )
