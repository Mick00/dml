import logging
import os

from src.base.client.client_state_helpers import get_node_id
from src.base.client.messages.serializer import JSONSerializer
from src.base.logging.JsonFormatter import JsonFormatter
from src.base.logging.logging_helpers import get_log_folder, DML_LOGGER, LOGGING_MODULE, LOGGER_KEY, verbose_level
from src.base.states.event import Event
from src.base.states.state import State
from src.base.states.event_handler import EventHandlerSimple, Handler


class InitLogger(EventHandlerSimple):
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

