from src.datasets.data_helpers import DATA_MODULE
from src.datasets.data_loader import DataLoader, DATALOADER_KEY
from src.datasets.events import DataRegisterHook
from src.protocol.states.event import Event
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition


class InitDataLoader(StateTransition):
    def transition(self, event: Event, state: State, handler: Handler):
        data_loader = DataLoader()
        state.update_module(DATA_MODULE, {
            DATALOADER_KEY: data_loader
        })
        handler.queue_event(DataRegisterHook())