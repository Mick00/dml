from src.nsclust.events import AggregationCompleted
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandlerSimple
from src.base.training.events import NextRound


class CloseRound(EventHandlerSimple):
    def transition(self, event: AggregationCompleted, state: State, handler: EventListener):
        handler.queue_event(NextRound(event.round_id))
