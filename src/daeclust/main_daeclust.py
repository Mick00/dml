from dotenv import load_dotenv

from src.daeclust.register import register_daeclust_module
from src.datasets.register import register_data_module
from src.nsclust.register import register_nsclust_module
from src.protocol.cli.cli import register_cli_module
from src.protocol.cli.constant import CLI_START
from src.protocol.client.reducers import register_client_module
from src.protocol.config.cli_config import get_arg_parse
from src.protocol.config.config import register_config_module, UpdateConfig
from src.protocol.states.event import Event
from src.protocol.states.handler import Handler
from src.protocol.states.reducers import HANDLER_START, register_handler_module
from src.protocol.training.register import register_training_module

parser = get_arg_parse()

if __name__ == '__main__':
    args = parser.parse_args()
    load_dotenv()
    handler = Handler()
    register_config_module(handler)
    register_handler_module(handler)
    register_cli_module(handler)
    register_data_module(handler)
    register_client_module(handler)
    register_training_module(handler)
    register_daeclust_module(handler)
    handler.handle_event(UpdateConfig(args.__dict__))
    handler.handle_event(Event(HANDLER_START))
    handler.handle_event(Event(CLI_START))