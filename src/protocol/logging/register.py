from src.protocol.client.actions.constants import NEW_PEER
from src.protocol.config.cli_config import get_arg_parse
from src.protocol.logging.log_handler import LogInfoHandler, LOG_INFO, LOG_WARNING, LogWarningHandler
from src.protocol.logging.log_new_peer import LogNewPeer
from src.protocol.logging.log_start_round import LogStartRound
from src.protocol.logging.log_training import LogStartTraining, LogCompletedTraining
from src.protocol.logging.logger import InitLogger
from src.protocol.states.constants import HANDLER_STARTED
from src.protocol.states.handler import Handler
from src.protocol.training.constants import ROUND_START, TRAIN_MODEL, MODEL_TRAINED

arg_parse = get_arg_parse()
arg_parse.add_argument("--logs")
arg_parse.add_argument("--debug", type=bool, default=False)


def register_logging_module(handler: Handler):
    handler.register_reducer(HANDLER_STARTED, InitLogger(11))
    handler.register_reducer(LOG_INFO, LogInfoHandler(10))
    handler.register_reducer(LOG_WARNING, LogWarningHandler(10))
    handler.register_reducer(NEW_PEER, LogNewPeer(10))
    handler.register_reducer(ROUND_START, LogStartRound(10))
    handler.register_reducer(TRAIN_MODEL, LogStartTraining(10))
    handler.register_reducer(MODEL_TRAINED, LogCompletedTraining(10))