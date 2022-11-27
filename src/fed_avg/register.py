from src.datasets.events import DATA_REGISTER_HOOK
from src.datasets.trigger_dataset_prepare import TriggerDatasetPrepare
from src.fed_avg.configure_dataset import ConfigureDataset
from src.nsclust.aggregate import Aggregate
from src.nsclust.close_round import CloseRound
from src.nsclust.constants import START_SELECTION, UPDATES_SELECTED, AGGREGATION_DONE
from src.fed_avg.init_tracking import InitTracking
from src.fed_avg.start_training import StartTrainingPhase
from src.nsclust.storage.init_model_storage import InitModelLoader
from src.fed_avg.accept_updates import AcceptAllUpdates
from src.fed_avg.constant import AGGREGATE_TEST_DONE
from src.fed_avg.start_aggregation import FedAvgStartAgg
from src.fed_avg.test_aggregate import TestAggregate
from src.protocol.client.constants import CLIENT_STARTED
from src.protocol.states.constants import HANDLER_STARTED
from src.protocol.states.handler import Handler
from src.protocol.training.constants import ROUND_START, MODEL_TRAINED, NEXT_ROUND
from src.protocol.training.fedml.constants import TRAINING_UPDATE_QUEUED, TRAINING_UPDATE_SHARE
from src.protocol.training.fedml.share_update import ShareUpdate, ReceiveUpdate


def register_fed_avg_module(handler: Handler):
    handler.register_reducer(CLIENT_STARTED, InitModelLoader(30))
    handler.register_reducer(HANDLER_STARTED, InitTracking(70))
    handler.register_reducer(DATA_REGISTER_HOOK, ConfigureDataset(100))
    handler.register_reducer(NEXT_ROUND, TriggerDatasetPrepare(100))
    handler.register_reducer(ROUND_START, StartTrainingPhase(100))
    handler.register_reducer(MODEL_TRAINED, ShareUpdate(200))
    handler.register_reducer(TRAINING_UPDATE_SHARE, ReceiveUpdate(100))
    handler.register_reducer(TRAINING_UPDATE_QUEUED, FedAvgStartAgg(100))
    handler.register_reducer(START_SELECTION, AcceptAllUpdates(100))
    handler.register_reducer(UPDATES_SELECTED, Aggregate(100))
    handler.register_reducer(AGGREGATION_DONE, TestAggregate(100))
    handler.register_reducer(AGGREGATE_TEST_DONE, CloseRound(100))
