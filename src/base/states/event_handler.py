import logging
from abc import ABC, abstractmethod
import time
from logging import Logger

from ..logging.logging_helpers import get_logger
from ..states.state import State
from ..states.event import Event


class Handler:
    pass


class EventHandlerSimple(ABC):
    def __init__(self, priority):
        self.priority = priority

    @abstractmethod
    def transition(self, event: Event, state: State, handler: Handler):
        pass


class EventHandler(EventHandlerSimple):

    def transition(self, event: Event, state: State, handler: Handler):
        start = time.time()
        logs = self._transition(event, state, handler)
        end = time.time()
        logger = get_logger(state)
        logger.debug(self.__class__.__name__, extra={"execution_time": end - start})
        if logs is not None:
            self.submit_logs(logger, logs)

    def log_info(self, msg, extra=None):
        return self.log(msg, logging.INFO, extra)

    def log(self, msg, level, extra=None):
        return {
            "level": level,
            "msg": msg,
            "extra": extra
        }

    def submit_logs(self, logger: Logger, logs: [dict]):
        for log in logs:
            logger.log(level=log.get("level", logging.INFO), msg=log.get("msg"), extra=log.get("extra", None))

    @abstractmethod
    def _transition(self, event: Event, state: State, handler: Handler) -> [dict]:
        pass
