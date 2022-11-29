from src.protocol.states.constants import HANDLER_STOP
from src.protocol.states.event import Event
from src.protocol.states.state import State
from src.protocol.states.handler import Handler
from src.protocol.states.transition import StateTransition


class TriggerStop(StateTransition):
    def transition(self, msg: Event, state: State, handler: Handler):
        handler.queue_event(Event(HANDLER_STOP))
