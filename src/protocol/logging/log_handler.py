from datetime import datetime

from src.protocol.logging.logger import get_logger
from src.protocol.states.event import Event
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition


LOG_INFO = "logging.log.info"


class Log(Event):
    def __init__(self, type, msg, extra=None):
        super(Log, self).__init__(type)
        extra = extra if not None else {}
        now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        extra["timestamp"] = now
        self.msg = msg
        self.extra = extra


class LogInfo(Log):
    def __init__(self, msg, extra=None):
        super(LogInfo, self).__init__(LOG_INFO, msg, extra)


class LogInfoHandler(StateTransition):
    def transition(self, event: LogInfo, state: State, handler: Handler):
        get_logger(state).info(event.msg, extra=event.extra)
