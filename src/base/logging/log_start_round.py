from src.base.logging.logging_helpers import get_logger
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandlerSimple
from src.base.training.events import StartRound


class LogStartRound(EventHandlerSimple):
    def transition(self, event: StartRound, state: State, handler: EventListener):
        get_logger(state).info(event.type, extra={"round_id": event.round_id})