from src.protocol.client.actions.constants import NEW_PEER
from src.protocol.config.cli_config import get_arg_parse
from src.protocol.logging.log_new_peer import LogNewPeer
from src.protocol.logging.logger import InitLogger
from src.protocol.states.constants import HANDLER_STARTED
from src.protocol.states.handler import Handler

arg_parse = get_arg_parse()
arg_parse.add_argument("--logs")
arg_parse.add_argument("--debug", type=bool, default=False)


def register_logging_module(handler: Handler):
    handler.register_reducer(HANDLER_STARTED, InitLogger(11))
    handler.register_reducer(NEW_PEER, LogNewPeer(10))
