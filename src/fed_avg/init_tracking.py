from src.base.config.config_state_helper import get_experience_name
from src.base.states.event import Event
from src.base.states.handler import Handler
from src.base.states.state import State
from src.base.states.transition import StateTransition
from src.base.training.events import InitExperiment


class InitTracking(StateTransition):
    def transition(self, event: Event, state: State, handler: Handler):
        handler.queue_event(InitExperiment(get_experience_name(state)))