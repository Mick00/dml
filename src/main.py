from dotenv import load_dotenv

from src.daeclust.register import register_daeclust_module
from src.fed_avg.register import register_fed_avg_module
from src.protocol.cli.cli import register_cli_module
from src.protocol.cli.constant import CLI_START
from src.protocol.client.reducers import register_client_module
from src.protocol.config.config import register_config_module, UpdateConfig
from src.protocol.states.event import Event
from src.protocol.states.handler import Handler
from src.protocol.states.reducers import HANDLER_START, register_handler_module

import argparse

from src.protocol.training.register import register_training_module

parser = argparse.ArgumentParser(description='Launch a decentralised ML node')
parser.add_argument('--data_path')
parser.add_argument('--broker_hostname')
parser.add_argument('--broker_port', type=int, default=5672)
parser.add_argument('--trainer_threshold', type=int)
parser.add_argument('--local_model')
parser.add_argument('--training_out')
parser.add_argument('--tracking_uri', default="http://localhost:5000")
parser.add_argument('--experiment_name', default="declust")

if __name__ == '__main__':
    args = parser.parse_args()
    load_dotenv()
    handler = Handler()
    register_config_module(handler)
    register_handler_module(handler)
    register_cli_module(handler)
    register_client_module(handler)
    register_training_module(handler)
    register_fed_avg_module(handler)
    handler.handle_event(UpdateConfig(args.__dict__))
    handler.handle_event(Event(HANDLER_START))
    handler.handle_event(Event(CLI_START))