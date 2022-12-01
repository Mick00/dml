from src.base.client.actions.constants import NEW_PEER
from src.base.config.cli_config import get_arg_parse
from src.base.logging.log_handler import LogInfoHandler, LOG_INFO, LOG_WARNING, LogWarningHandler
from src.base.logging.log_new_peer import LogNewPeer
from src.base.logging.log_start_round import LogStartRound
from src.base.logging.log_training import LogStartTraining, LogCompletedTraining
from src.base.logging.logger import InitLogger
from src.base.states.constants import HANDLER_STARTED
from src.base.states.handler import Handler
from src.base.training.constants import ROUND_START, TRAIN_MODEL, MODEL_TRAINED

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