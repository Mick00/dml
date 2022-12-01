from src.base.datasets.events import PrepareDataset
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandler
from src.base.training.events import NextRound


class TriggerDatasetPrepare(EventHandler):
    def transition(self, event: NextRound, state: State, handler: EventListener):
        if event.current_round == -1:
            handler.queue_event(PrepareDataset())
