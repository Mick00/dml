from src.base.client.constants import CLIENT_STARTED
from src.base.config.cli_config import get_arg_parse
from src.base.datasets.events import DATASET_PREPARE
from src.base.datasets.sampler_conf.sampler_configurator import ConfigureSampler
from src.base.datasets.trigger_dataset_prepare import TriggerDatasetPrepare
from src.base.states.constants import HANDLER_STARTED
from src.base.states.event_listener import EventListener
from src.base.training.constants import NEXT_ROUND, ROUND_START, MODEL_TRAINED
from src.base.training.fedml.share_update import ShareUpdate
from src.fschain.handlers.round_start.start_training_phase import StartTrainingPhase
from src.fschain.senders import RegisterChainAdapters
from src.nsclust.init_tracking import InitTracking
from src.nsclust.storage.init_model_storage import InitModelLoader
from src.daeclust.state.init_strategy import InitStrategy, InitStrategyForRound

argparse = get_arg_parse()
#argparse.add_argument('--divergence_tolerance', default="3")
#argparse.add_argument('--cluster_metric', required=True)
#argparse.add_argument('--cluster_scoring', required=True)
#argparse.add_argument('--divergence_method', default=None)

def register_fschain(handler: EventListener):
    handler.register_handler(CLIENT_STARTED, RegisterChainAdapters(20))
    handler.register_handler(CLIENT_STARTED, InitModelLoader(30))
    handler.register_handler(HANDLER_STARTED, InitTracking(70))
    handler.register_handler(DATASET_PREPARE, ConfigureSampler(50))
    handler.register_handler(CLIENT_STARTED, InitStrategy(71))
    handler.register_handler(NEXT_ROUND, TriggerDatasetPrepare(100))
    handler.register_handler(ROUND_START, InitStrategyForRound(90))
    handler.register_handler(ROUND_START, StartTrainingPhase(100))
    handler.register_handler(MODEL_TRAINED, ShareUpdate(200))