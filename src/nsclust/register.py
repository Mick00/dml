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
from src.base.client.constants import CLIENT_STARTED
from src.base.states.constants import HANDLER_STARTED
from src.base.states.event_listener import EventListener
from src.base.training.constants import ROUND_START, MODEL_TRAINED
from src.base.training.fedml.constants import TRAINING_UPDATE_QUEUED, TRAINING_UPDATE_SHARE
from src.base.training.fedml.share_update import ShareUpdate, ReceiveUpdate


def register_nsclust_module(handler: EventListener):
    handler.register_handler(CLIENT_STARTED, InitModelLoader(30))
    handler.register_handler(HANDLER_STARTED, InitTracking(70))
    handler.register_handler(ROUND_START, StartTrainingPhase(100))
    handler.register_handler(CLUSTER_SELECTION, StartClusterSelectionTests(100))
    handler.register_handler(CLUSTER_TEST_COMPLETED, SelectBestCluster(100))
    handler.register_handler(MODEL_TRAINED, ShareUpdate(200))
    handler.register_handler(TRAINING_UPDATE_SHARE, ReceiveUpdate(100))
    handler.register_handler(TRAINING_UPDATE_QUEUED, StartUpdateSelectionTransition(100))
    handler.register_handler(START_SELECTION, AcceptAllUpdates(100))
    handler.register_handler(UPDATES_SELECTED, Aggregate(100))
    handler.register_handler(AGGREGATION_DONE, CloseRound(100))
