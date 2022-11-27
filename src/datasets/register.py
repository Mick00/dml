from src.datasets.dataset_prepare import DatasetPrepare
from src.datasets.events import DATASET_PREPARE, DATA_REGISTER_HOOK
from src.datasets.init_data_loader import InitDataLoader
from src.datasets.loaders.emnist_loader import EmnistRegister
from src.datasets.loaders.mnist_loader import MnistRegister
from src.protocol.config.cli_config import get_arg_parse
from src.protocol.states.constants import HANDLER_STARTED
from src.protocol.states.handler import Handler


parser = get_arg_parse()
parser.add_argument('--data_path')
parser.add_argument('--dataset')

def register_data_module(handler: Handler):
    handler.register_reducer(HANDLER_STARTED, InitDataLoader(50))
    handler.register_reducer(DATASET_PREPARE, DatasetPrepare(100))
    handler.register_reducer(DATA_REGISTER_HOOK, MnistRegister(100))
    handler.register_reducer(DATA_REGISTER_HOOK, EmnistRegister(100))
