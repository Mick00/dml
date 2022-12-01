from src.base.datasets.data_helpers import DATA_MODULE
from src.base.datasets.data_loader import DataLoader, DATALOADER_KEY
from src.base.datasets.events import DataRegisterHook
from src.base.states.event import Event
from src.base.states.handler import Handler
from src.base.states.state import State
from src.base.states.transition import StateTransition


class InitDataLoader(StateTransition):
    def transition(self, event: Event, state: State, handler: Handler):
        data_loader = DataLoader()
        state.update_module(DATA_MODULE, {
            DATALOADER_KEY: data_loader
        })
        handler.queue_event(DataRegisterHook())