from src.datasets.events import PrepareDataset
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition
from src.protocol.training.events import NextRound


class TriggerDatasetPrepare(StateTransition):
    def transition(self, event: NextRound, state: State, handler: Handler):
        if event.current_round == -1:
            handler.queue_event(PrepareDataset())
