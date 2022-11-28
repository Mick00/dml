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
parser.add_argument('--data_balance', type=bool, default=False)
parser.add_argument('--data_n_partitions', type=int, default=-1)
parser.add_argument('--data_partition_index', type=int, default=-1)
parser.add_argument('--data_lower_bound', type=int, default=-1)
parser.add_argument('--data_higher_bound', type=int, default=-1)
parser.add_argument('--data_mean', type=int, default=-1)
parser.add_argument('--data_std', type=int, default=-1)


def register_data_module(handler: Handler):
    handler.register_reducer(HANDLER_STARTED, InitDataLoader(80))
    handler.register_reducer(DATASET_PREPARE, DatasetPrepare(100))
    handler.register_reducer(DATA_REGISTER_HOOK, MnistRegister(100))
    handler.register_reducer(DATA_REGISTER_HOOK, EmnistRegister(100))
