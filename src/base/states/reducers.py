from threading import Thread

from .constants import HANDLER_START, HANDLER_STOP, HANDLER_MODULE, HANDLER_STARTED
from ..states.event import Event
from ..states.handler import Handler
from ..states.state import State
from ..states.transition import StateTransition


def register_handler_module(handler: Handler):
    handler.register_reducer(HANDLER_START, StartHandler(0))
    handler.register_reducer(HANDLER_STOP, StopHandler(100))


class StartHandler(StateTransition):

    def transition(self, event: Event, state: State, handler: Handler):
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


class StopHandler(StateTransition):

    def transition(self, event: Event, state: State, handler: Handler):
        state.update_module(HANDLER_MODULE, {
            "started": False,
        })