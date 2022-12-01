from src.base.states.constants import HANDLER_STOP
from src.base.states.event import Event
from src.base.states.state import State
from src.base.states.event_listener import EventListener
from src.base.states.event_handler import EventHandler


class TriggerStop(EventHandler):
    def transition(self, msg: Event, state: State, handler: EventListener):
        handler.queue_event(Event(HANDLER_STOP))
