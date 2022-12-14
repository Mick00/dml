from dotenv import load_dotenv

from src.base.datasets.register import register_data_module
from src.fed_avg.register import register_fed_avg_module
from src.base.cli.cli import register_cli_module
from src.base.cli.constant import CLI_START
from src.base.client.reducers import register_client_module
from src.base.config.cli_config import get_arg_parse
from src.base.config.config import register_config_module, UpdateConfig
from src.base.logging.register import register_logging_module
from src.base.states.event import Event
from src.base.states.event_listener import EventListener
from src.base.states.handlers import HANDLER_START, register_handler_module
from src.base.training.register import register_training_module

parser = get_arg_parse()


def bootstrap_fed_avg():
    args = parser.parse_args()
    load_dotenv()
    event_listener = EventListener()
    register_logging_module(event_listener)
    register_config_module(event_listener)
    register_handler_module(event_listener)
    if args.interactive:
        register_cli_module(event_listener)
    register_data_module(event_listener)
    register_client_module(event_listener)
    register_training_module(event_listener)
    register_fed_avg_module(event_listener)
    event_listener.handle_event(UpdateConfig(args.__dict__))
    event_listener.handle_event(Event(HANDLER_START))
    if args.interactive:
        event_listener.handle_event(Event(CLI_START))


if __name__ == '__main__':
    bootstrap_fed_avg()