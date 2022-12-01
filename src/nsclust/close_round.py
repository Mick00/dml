from src.nsclust.events import AggregationCompleted
from src.base.states.handler import Handler
from src.base.states.state import State
from src.base.states.transition import StateTransition
from src.base.training.events import NextRound


class CloseRound(StateTransition):
    def transition(self, event: AggregationCompleted, state: State, handler: Handler):
        handler.queue_event(NextRound(event.round_id))
