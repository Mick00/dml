from src.nsclust.aggregate import Aggregate
from src.nsclust.close_round import CloseRound
from src.nsclust.constants import START_SELECTION, UPDATES_SELECTED, CLUSTER_SELECTION, CLUSTER_TEST_COMPLETED, \
    AGGREGATION_DONE
from src.nsclust.init_tracking import InitTracking
from src.nsclust.select_cluster import StartClusterSelectionTests, SelectBestCluster
from src.nsclust.select_updates import AcceptAllUpdates
from src.nsclust.start_selection import StartUpdateSelectionTransition
from src.nsclust.start_training import StartTrainingPhase
from src.nsclust.storage.init_model_storage import InitModelLoader
from src.protocol.client.constants import CLIENT_STARTED
from src.protocol.states.constants import HANDLER_STARTED
from src.protocol.states.handler import Handler
from src.protocol.training.constants import ROUND_START, MODEL_TRAINED
from src.protocol.training.fedml.constants import TRAINING_UPDATE_QUEUED, TRAINING_UPDATE_SHARE
from src.protocol.training.fedml.share_update import ShareUpdate, ReceiveUpdate


def register_nsclust_module(handler: Handler):
    handler.register_reducer(CLIENT_STARTED, InitModelLoader(30))
    handler.register_reducer(HANDLER_STARTED, InitTracking(70))
    handler.register_reducer(ROUND_START, StartTrainingPhase(100))
    handler.register_reducer(CLUSTER_SELECTION, StartClusterSelectionTests(100))
    handler.register_reducer(CLUSTER_TEST_COMPLETED, SelectBestCluster(100))
    handler.register_reducer(MODEL_TRAINED, ShareUpdate(200))
    handler.register_reducer(TRAINING_UPDATE_SHARE, ReceiveUpdate(100))
    handler.register_reducer(TRAINING_UPDATE_QUEUED, StartUpdateSelectionTransition(100))
    handler.register_reducer(START_SELECTION, AcceptAllUpdates(100))
    handler.register_reducer(UPDATES_SELECTED, Aggregate(100))
    handler.register_reducer(AGGREGATION_DONE, CloseRound(100))
