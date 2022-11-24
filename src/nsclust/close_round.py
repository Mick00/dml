from src.nsclust.events import AggregationCompleted
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition
from src.protocol.training.events import NextRound


class CloseRound(StateTransition):
    def transition(self, event: AggregationCompleted, state: State, handler: Handler):
        handler.queue_event(NextRound(event.round_id))
