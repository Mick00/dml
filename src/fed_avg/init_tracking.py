from src.base.config.config_state_helper import get_experience_name
from src.base.states.event import Event
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandlerSimple
from src.base.training.events import InitExperiment


class InitTracking(EventHandlerSimple):
    def transition(self, event: Event, state: State, handler: EventListener):
        handler.queue_event(InitExperiment(get_experience_name(state)))