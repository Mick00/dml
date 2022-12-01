from datetime import datetime

from src.base.logging.logging_helpers import get_logger
from src.base.states.event import Event
from src.base.states.handler import Handler
from src.base.states.state import State
from src.base.states.transition import StateTransition


LOG_INFO = "logging.log.info"
LOG_WARNING = "logging.log.warning"


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


class LogWarning(Log):
    def __init__(self, msg, extra=None):
        super(LogWarning, self).__init__(LOG_WARNING, msg, extra)


class LogInfoHandler(StateTransition):
    def transition(self, event: LogInfo, state: State, handler: Handler):
        get_logger(state).info(event.msg, extra=event.extra)


class LogWarningHandler(StateTransition):
    def transition(self, event: LogInfo, state: State, handler: Handler):
        get_logger(state).warning(event.msg, extra=event.extra)
