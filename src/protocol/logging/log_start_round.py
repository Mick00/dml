from src.protocol.logging.logger import get_logger
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition
from src.protocol.training.events import StartRound


class LogStartRound(StateTransition):
    def transition(self, event: StartRound, state: State, handler: Handler):
        get_logger(state).info(event.type, extra={"round_id": event.round_id})