import time
from queue import Queue
import signal

from src.base.states.constants import HANDLER_MODULE, HANDLER_STOPPED, HANDLER_STOP
from src.base.states.state import State
from src.base.states.event import Event
from src.base.states.event_handler import EventHandlerSimple


class EventListener:

    def __init__(self):
        self.handlers = {}
        self.state = State()
        self.event_queue = Queue()
        signal.signal(signal.SIGINT, self.exit_graceful)
        signal.signal(signal.SIGTERM, self.exit_graceful)

    def register_handler(self, message_type, reducer: EventHandlerSimple):
        if message_type in self.handlers:
            self.handlers[message_type].append(reducer)
            self.handlers[message_type].sort(key=lambda reducer: reducer.priority)
        else:
            self.handlers[message_type] = [reducer]

    def get_handlers(self, event_type: str):
        if event_type in self.handlers:
            return self.handlers[event_type]
        else:
            return []

    def queue_event(self, message: Event):
        self.event_queue.put(message)

    def handle_event(self, message: Event):
        reducers = self.get_handlers(message.type)
        for reducer in reducers:
            reducer.transition(message, self.state, self)

    def handle_events(self):
        while self.state.get_module_state(HANDLER_MODULE)["started"]:
            event = self.event_queue.get()
            if event:
                self.handle_event(event)
            else:
                time.sleep(0.25)
        self.handle_event(Event(HANDLER_STOPPED))

    def exit_graceful(self, signum, frame):
        self.stop()

    def stop(self):
        self.queue_event(Event(HANDLER_STOP))