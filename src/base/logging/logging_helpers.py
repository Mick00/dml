import logging

from src.base.config.config_state_helper import get_config
from src.base.states.state import State


DML_LOGGER = "dml"
LOGGING_MODULE = "logging"
LOGGER_KEY = "logger"


def get_log_folder(state: State) -> str:
    return get_config(state).get("logs")

def debug_enable(state: State) -> bool:
    return get_config(state).get("debug")


def verbose_level(state: State) -> int:
    return logging.DEBUG if debug_enable(state) else logging.INFO


def get_logger(state: State) -> logging.Logger:
    return state.get_module_state(LOGGING_MODULE).get(LOGGER_KEY)
