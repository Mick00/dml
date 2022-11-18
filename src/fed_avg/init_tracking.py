from src.protocol.config.config_state_helper import get_experience_name
from src.protocol.states.event import Event
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition
from src.protocol.training.events import InitExperiment


class InitTracking(StateTransition):
    def transition(self, event: Event, state: State, handler: Handler):
        handler.queue_event(InitExperiment(get_experience_name(state)))