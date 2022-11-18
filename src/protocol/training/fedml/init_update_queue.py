from src.protocol.states.event import Event
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition, Handler
from src.protocol.training.constants import TRAINING_MODULE
from src.protocol.training.fedml.fedml_state_helper import UPDATE_QUEUE_KEY
from src.protocol.training.fedml.update_queue import UpdateQueue


class InitUpdateQueue(StateTransition):
    def transition(self, event: Event, state: State, handler: Handler):
        state.update_module(TRAINING_MODULE, {UPDATE_QUEUE_KEY: UpdateQueue(handler)})
