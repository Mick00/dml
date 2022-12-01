from threading import Thread

from .constants import HANDLER_START, HANDLER_STOP, HANDLER_MODULE, HANDLER_STARTED
from ..states.event import Event
from ..states.event_listener import EventListener
from ..states.state import State
from ..states.event_handler import EventHandlerSimple


def register_handler_module(handler: EventListener):
    handler.register_handler(HANDLER_START, StartHandler(0))
    handler.register_handler(HANDLER_STOP, StopHandler(100))


class StartHandler(EventHandlerSimple):

    def transition(self, event: Event, state: State, handler: EventListener):
        mod_state = state.get_module_state(HANDLER_MODULE)
        started = mod_state["started"] if "started" in mod_state else False
        if not started:
            handler_thread = Thread(target=handler.handle_events, args=())
            handler_thread.setName("handler")
            state.update_module(HANDLER_MODULE, {
                "started": True,
                "thread": handler_thread
            })
            handler_thread.start()
            handler.queue_event(Event(HANDLER_STARTED))


class StopHandler(EventHandlerSimple):

    def transition(self, event: Event, state: State, handler: EventListener):
        state.update_module(HANDLER_MODULE, {
            "started": False,
        })