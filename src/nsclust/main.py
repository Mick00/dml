from dotenv import load_dotenv

from src.nsclust.register import register_nsclust_module
from src.base.cli.cli import register_cli_module
from src.base.cli.constant import CLI_START
from src.base.client.reducers import register_client_module
from src.base.config.cli_config import get_arg_parse
from src.base.config.config import register_config_module, UpdateConfig
from src.base.states.event import Event
from src.base.states.event_listener import EventListener
from src.base.states.handlers import HANDLER_START, register_handler_module
from src.base.training.register import register_training_module

parser = get_arg_parse()

if __name__ == '__main__':
    args = parser.parse_args()
    load_dotenv()
    handler = EventListener()
    register_config_module(handler)
    register_handler_module(handler)
    register_cli_module(handler)
    register_client_module(handler)
    register_training_module(handler)
    register_nsclust_module(handler)
    handler.handle_event(UpdateConfig(args.__dict__))
    handler.handle_event(Event(HANDLER_START))
    handler.handle_event(Event(CLI_START))