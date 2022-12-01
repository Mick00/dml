from src.base.states.constants import HANDLER_STOP
from src.base.states.event import Event
from src.base.states.state import State
from src.base.states.handler import Handler
from src.base.states.transition import StateTransition


class TriggerStop(StateTransition):
    def transition(self, msg: Event, state: State, handler: Handler):
        handler.queue_event(Event(HANDLER_STOP))
