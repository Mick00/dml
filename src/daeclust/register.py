from src.daeclust.constants import AGGREGATION_UPDATE_POOLED, AGGREGATION_UPDATE_SELECTION_START, AGGREGATION_UPDATE_SELECTION_DONE
from src.daeclust.state.handle_new_updates import UpdateHandler
from src.daeclust.state.handle_selected_updates import SelectedUpdatesHandler
from src.daeclust.state.init_strategy import InitStrategy, InitStrategyForRound
from src.daeclust.state.trigger_next_round import TriggerNextRound
from src.daeclust.state.trigger_update_selection import TriggerUpdateSelection
from src.daeclust.state.select_updates import WDUpdateSelector
from src.base.datasets.trigger_dataset_prepare import TriggerDatasetPrepare
from src.nsclust.constants import CLUSTER_SELECTION, CLUSTER_TEST_COMPLETED
from src.nsclust.init_tracking import InitTracking
from src.daeclust.state.select_cluster import StartClusterSelectionTests, SelectBestCluster
from src.daeclust.state.start_training import StartTrainingPhase
from src.base.client.constants import CLIENT_STARTED
from src.base.states.constants import HANDLER_STARTED
from src.base.states.handler import Handler
from src.base.training.constants import ROUND_START, MODEL_TRAINED, NEXT_ROUND
from src.base.training.fedml.constants import TRAINING_UPDATE_SHARE
from src.base.training.fedml.share_update import ShareUpdate


def register_daeclust_module(handler: Handler):
    handler.register_reducer(HANDLER_STARTED, InitTracking(70))
    handler.register_reducer(CLIENT_STARTED, InitStrategy(71))
    handler.register_reducer(NEXT_ROUND, TriggerDatasetPrepare(100))
    handler.register_reducer(ROUND_START, StartTrainingPhase(100))
    handler.register_reducer(ROUND_START, InitStrategyForRound(90))
    handler.register_reducer(CLUSTER_SELECTION, StartClusterSelectionTests(100))
    handler.register_reducer(CLUSTER_TEST_COMPLETED, SelectBestCluster(100))
    handler.register_reducer(MODEL_TRAINED, ShareUpdate(200))
    handler.register_reducer(TRAINING_UPDATE_SHARE, UpdateHandler(100))
    handler.register_reducer(AGGREGATION_UPDATE_POOLED, TriggerUpdateSelection(100))
    handler.register_reducer(AGGREGATION_UPDATE_SELECTION_START, WDUpdateSelector(100))
    handler.register_reducer(AGGREGATION_UPDATE_SELECTION_DONE, SelectedUpdatesHandler(100))
    handler.register_reducer(AGGREGATION_UPDATE_SELECTION_DONE, TriggerNextRound(110))
