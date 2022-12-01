from src.base.logging.logging_helpers import get_logger
from src.base.states.handler import Handler
from src.base.states.state import State
from src.base.states.transition import StateTransition
from src.base.training.events import StartRound


class LogStartRound(StateTransition):
    def transition(self, event: StartRound, state: State, handler: Handler):
        get_logger(state).info(event.type, extra={"round_id": event.round_id})