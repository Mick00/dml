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
from src.base.states.handler import Handler
from src.base.states.reducers import HANDLER_START, register_handler_module
from src.base.training.register import register_training_module

parser = get_arg_parse()


def bootstrap_fed_avg():
    args = parser.parse_args()
    load_dotenv()
    handler = Handler()
    register_logging_module(handler)
    register_config_module(handler)
    register_handler_module(handler)
    if args.interactive:
        register_cli_module(handler)
    register_data_module(handler)
    register_client_module(handler)
    register_training_module(handler)
    register_fed_avg_module(handler)
    handler.handle_event(UpdateConfig(args.__dict__))
    handler.handle_event(Event(HANDLER_START))
    if args.interactive:
        handler.handle_event(Event(CLI_START))


if __name__ == '__main__':
    bootstrap_fed_avg()