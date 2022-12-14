from torchvision import datasets
from torchvision.transforms import ToTensor

from src.base.datasets.data_helpers import get_data_path
from src.base.datasets.data_loader import get_data_loader
from src.base.states.event import Event
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandlerSimple


class EmnistRegister(EventHandlerSimple):
    def transition(self, event: Event, state: State, handler: EventListener):
        data_loader = get_data_loader(state)
        data_loader.register_loader("emnist", lambda state: load_emnist(get_data_path(state)))


def load_emnist(data_path: str):
    if not data_path:
        raise Exception("Data path is not set")
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
