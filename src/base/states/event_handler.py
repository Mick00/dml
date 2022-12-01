from abc import ABC, abstractmethod

from ..states.state import State
from ..states.event import Event


class Handler:
    pass


class EventHandler(ABC):
    def __init__(self, priority):
        self.priority = priority

    @abstractmethod
    def transition(self, event: Event, state: State, handler: Handler):
        pass
