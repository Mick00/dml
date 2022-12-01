from src.base.datasets.events import PrepareDataset
from src.base.states.handler import Handler
from src.base.states.state import State
from src.base.states.transition import StateTransition
from src.base.training.events import NextRound


class TriggerDatasetPrepare(StateTransition):
    def transition(self, event: NextRound, state: State, handler: Handler):
        if event.current_round == -1:
            handler.queue_event(PrepareDataset())
