from src.base.datasets.dataset_prepare import DatasetPrepare
from src.base.datasets.events import DATASET_PREPARE, DATA_REGISTER_HOOK
from src.base.datasets.init_data_loader import InitDataLoader
from src.base.datasets.loaders.emnist_loader import EmnistRegister
from src.base.datasets.loaders.fmnist_loader import FmnistRegister
from src.base.datasets.loaders.mnist_loader import MnistRegister
from src.base.config.cli_config import get_arg_parse
from src.base.states.constants import HANDLER_STARTED
from src.base.states.event_listener import EventListener


parser = get_arg_parse()
parser.add_argument('--data_path')
parser.add_argument('--dataset')
parser.add_argument('--data_balance', type=bool, default=False)
parser.add_argument('--data_n_partitions', type=int, default=-1)
parser.add_argument('--data_partition_index', type=int, default=-1)
parser.add_argument('--data_lower_bound', default="-1")
parser.add_argument('--data_higher_bound', default="-1")
parser.add_argument('--data_mean', default="-1")
parser.add_argument('--data_std', default="-1")
parser.add_argument('--n_samples', type=int, default=0)


def register_data_module(handler: EventListener):
    handler.register_handler(HANDLER_STARTED, InitDataLoader(80))
    handler.register_handler(DATASET_PREPARE, DatasetPrepare(100))
    handler.register_handler(DATA_REGISTER_HOOK, MnistRegister(100))
    handler.register_handler(DATA_REGISTER_HOOK, EmnistRegister(100))
    handler.register_handler(DATA_REGISTER_HOOK, FmnistRegister(100))
