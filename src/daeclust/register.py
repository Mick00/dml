from src.daeclust.aggregate import Aggregate
from src.daeclust.close_round import CloseRound
from src.daeclust.constants import START_SELECTION, UPDATES_SELECTED, CLUSTER_SELECTION, CLUSTER_TEST_COMPLETED, \
    AGGREGATION_DONE
from src.daeclust.init_tracking import InitTracking
from src.daeclust.select_cluster import StartClusterSelectionTests, SelectBestCluster
from src.daeclust.select_updates import AcceptAllUpdates
from src.daeclust.start_selection import StartUpdateSelectionTransition
from src.daeclust.start_training import StartTrainingPhase
from src.daeclust.storage.init_model_storage import InitModelLoader
from src.protocol.client.constants import CLIENT_STARTED
from src.protocol.states.constants import HANDLER_STARTED
from src.protocol.states.handler import Handler
from src.protocol.training.constants import ROUND_START, MODEL_TRAINED
from src.protocol.training.fedml.constants import UPDATE_QUEUED_EVENT
from src.protocol.training.fedml.share_update import ShareUpdate


def register_daeclust_module(handler: Handler):
    handler.register_reducer(CLIENT_STARTED, InitModelLoader(30))
    handler.register_reducer(HANDLER_STARTED, InitTracking(70))
    handler.register_reducer(ROUND_START, StartTrainingPhase(100))
    handler.register_reducer(CLUSTER_SELECTION, StartClusterSelectionTests(100))
    handler.register_reducer(CLUSTER_TEST_COMPLETED, SelectBestCluster(100))
    handler.register_reducer(MODEL_TRAINED, ShareUpdate(200))
    handler.register_reducer(UPDATE_QUEUED_EVENT, StartUpdateSelectionTransition(100))
    handler.register_reducer(START_SELECTION, AcceptAllUpdates(100))
    handler.register_reducer(UPDATES_SELECTED, Aggregate(100))
    handler.register_reducer(AGGREGATION_DONE, CloseRound(100))
