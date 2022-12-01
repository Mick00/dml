from src.base.states.event import Event
from src.base.states.state import State
from src.base.states.event_handler import EventHandlerSimple, Handler
from src.base.training.constants import TRAINING_MODULE
from src.base.training.fedml.fedml_state_helper import UPDATE_QUEUE_KEY
from src.base.training.fedml.update_queue import UpdateQueue


class InitUpdateQueue(EventHandlerSimple):
    def transition(self, event: Event, state: State, handler: Handler):
        state.update_module(TRAINING_MODULE, {UPDATE_QUEUE_KEY: UpdateQueue(handler)})
