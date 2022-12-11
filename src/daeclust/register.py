from src.base.config.cli_config import get_arg_parse
from src.base.datasets.events import DATASET_PREPARE
from src.base.datasets.sampler_conf.sampler_configurator import ConfigureSampler
from src.daeclust.constants import AGGREGATION_UPDATE_POOLED, AGGREGATION_UPDATE_SELECTION_START, \
    AGGREGATION_UPDATE_SELECTION_DONE, CLUSTER_SELECTED, FLUSH_UPDATES, TRAINING_UPDATED_CLUSTERS
from src.daeclust.state.handle_new_updates import UpdateHandler
from src.daeclust.state.handle_selected_updates import SelectedUpdatesHandler
from src.daeclust.state.init_strategy import InitStrategy, InitStrategyForRound
from src.daeclust.state.selected_clusters import ModelTrainedBuffer, SelectedClustersHandler
from src.daeclust.state.trigger_next_round import TriggerNextRound
from src.daeclust.state.trigger_update_selection import TriggerUpdateSelection
from src.daeclust.state.select_updates import WDUpdateSelector
from src.base.datasets.trigger_dataset_prepare import TriggerDatasetPrepare
from src.nsclust.constants import CLUSTER_SELECTION, CLUSTER_TEST_COMPLETED
from src.nsclust.init_tracking import InitTracking
from src.daeclust.state.select_cluster import StartClusterSelectionTests, SelectHighestScoreCluster
from src.daeclust.state.start_training import StartTrainingPhase
from src.base.client.constants import CLIENT_STARTED
from src.base.states.constants import HANDLER_STARTED
from src.base.states.event_listener import EventListener
from src.base.training.constants import ROUND_START, MODEL_TRAINED, NEXT_ROUND
from src.nsclust.storage.init_model_storage import InitModelLoader

argparse = get_arg_parse()
argparse.add_argument('--divergence_tolerance', type=float, default=3)
argparse.add_argument('--cluster_metric')
argparse.add_argument('--cluster_scoring')

def register_daeclust_module(handler: EventListener):
    handler.register_handler(CLIENT_STARTED, InitModelLoader(30))
    handler.register_handler(HANDLER_STARTED, InitTracking(70))
    handler.register_handler(DATASET_PREPARE, ConfigureSampler(50))
    handler.register_handler(CLIENT_STARTED, InitStrategy(71))
    handler.register_handler(NEXT_ROUND, TriggerDatasetPrepare(100))
    handler.register_handler(ROUND_START, InitStrategyForRound(90))
    handler.register_handler(ROUND_START, StartTrainingPhase(100))
    handler.register_handler(CLUSTER_SELECTION, StartClusterSelectionTests(100))
    handler.register_handler(CLUSTER_TEST_COMPLETED, SelectHighestScoreCluster(100))
    handler.register_handler(CLUSTER_SELECTED, SelectedClustersHandler(100))
    update_buffer = ModelTrainedBuffer(200)
    handler.register_handler(MODEL_TRAINED, update_buffer)
    handler.register_handler(FLUSH_UPDATES, update_buffer)
    handler.register_handler(TRAINING_UPDATED_CLUSTERS, UpdateHandler(100))
    handler.register_handler(AGGREGATION_UPDATE_POOLED, TriggerUpdateSelection(100))
    handler.register_handler(AGGREGATION_UPDATE_SELECTION_START, WDUpdateSelector(100))
    handler.register_handler(AGGREGATION_UPDATE_SELECTION_DONE, SelectedUpdatesHandler(100))
    handler.register_handler(AGGREGATION_UPDATE_SELECTION_DONE, TriggerNextRound(110))
