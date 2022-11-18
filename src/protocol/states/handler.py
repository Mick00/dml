from queue import Queue

from src.protocol.states.constants import HANDLER_MODULE, HANDLER_STOPPED
from src.protocol.states.state import State
from src.protocol.states.event import Event
from src.protocol.states.transition import StateTransition


class Handler:

    def __init__(self):
        self.reducers = {}
        self.state = State()
        self.event_queue = Queue()

    def register_reducer(self, message_type, reducer: StateTransition):
        if message_type in self.reducers:
            self.reducers[message_type].append(reducer)
            self.reducers[message_type].sort(key=lambda reducer: reducer.priority)
        else:
            self.reducers[message_type] = [reducer]

    def get_reducers(self, event_type: str):
        if event_type in self.reducers:
            return self.reducers[event_type]
        else:
            return []

    def queue_event(self, message: Event):
        self.event_queue.put(message)

    def handle_event(self, message: Event):
        reducers = self.get_reducers(message.type)
        for reducer in reducers:
            reducer.transition(message, self.state, self)

    def handle_events(self):
        while self.state.get_module_state(HANDLER_MODULE)["started"]:
            event = self.event_queue.get()
            self.handle_event(event)
        self.handle_event(Event(HANDLER_STOPPED))