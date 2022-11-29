import logging
import os

from pythonjsonlogger import jsonlogger

from src.protocol.client.client_state_helpers import get_node_id
from src.protocol.client.messages.serializer import JSONSerializer
from src.protocol.config.config_state_helper import get_config
from src.protocol.logging.JsonFormatter import JsonFormatter
from src.protocol.states.event import Event
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition, Handler

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


class InitLogger(StateTransition):
    def transition(self, event: Event, state: State, handler: Handler):
        logger = logging.getLogger(DML_LOGGER)
        basic_log_file, dml_log_file = self.get_log_paths(state)
        logging.basicConfig(level=verbose_level(state), filename=basic_log_file)
        log_file_handler = logging.FileHandler(dml_log_file)
        log_file_handler.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = JsonFormatter(json_encoder=JSONSerializer)
        log_file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        logger.addHandler(log_file_handler)
        logger.addHandler(console_handler)
        state.update_module(LOGGING_MODULE, {LOGGER_KEY: logger})

    def get_log_paths(self, state: State):
        folder = get_log_folder(state)
        node_id = get_node_id(state)
        if not os.path.exists(folder):
            os.makedirs(folder)
        return os.path.join(folder, f"{node_id}.log"), os.path.join(folder, f"dml-{node_id}.log")

