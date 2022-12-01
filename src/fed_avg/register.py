from src.base.datasets.events import DATASET_PREPARE
from src.base.datasets.trigger_dataset_prepare import TriggerDatasetPrepare
from src.base.datasets.sampler_conf.sampler_configurator import ConfigureSampler
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
from src.base.client.constants import CLIENT_STARTED
from src.base.states.constants import HANDLER_STARTED
from src.base.states.event_listener import EventListener
from src.base.training.constants import ROUND_START, MODEL_TRAINED, NEXT_ROUND
from src.base.training.fedml.constants import TRAINING_UPDATE_QUEUED, TRAINING_UPDATE_SHARE
from src.base.training.fedml.share_update import ShareUpdate, ReceiveUpdate


def register_fed_avg_module(handler: EventListener):
    handler.register_handler(CLIENT_STARTED, InitModelLoader(30))
    handler.register_handler(HANDLER_STARTED, InitTracking(70))
    handler.register_handler(DATASET_PREPARE, ConfigureSampler(50))
    handler.register_handler(NEXT_ROUND, TriggerDatasetPrepare(100))
    handler.register_handler(ROUND_START, StartTrainingPhase(100))
    handler.register_handler(MODEL_TRAINED, ShareUpdate(200))
    handler.register_handler(TRAINING_UPDATE_SHARE, ReceiveUpdate(100))
    handler.register_handler(TRAINING_UPDATE_QUEUED, FedAvgStartAgg(100))
    handler.register_handler(START_SELECTION, AcceptAllUpdates(100))
    handler.register_handler(UPDATES_SELECTED, Aggregate(100))
    handler.register_handler(AGGREGATION_DONE, TestAggregate(100))
    handler.register_handler(AGGREGATE_TEST_DONE, CloseRound(100))
