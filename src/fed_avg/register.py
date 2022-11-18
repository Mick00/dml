from src.daeclust.aggregate import Aggregate
from src.daeclust.close_round import CloseRound
from src.daeclust.constants import START_SELECTION, UPDATES_SELECTED, AGGREGATION_DONE
from src.fed_avg.init_tracking import InitTracking
from src.fed_avg.start_training import StartTrainingPhase
from src.daeclust.storage.init_model_storage import InitModelLoader
from src.fed_avg.accept_updates import AcceptAllUpdates
from src.fed_avg.constant import AGGREGATE_TEST_DONE
from src.fed_avg.start_aggregation import FedAvgStartAgg
from src.fed_avg.test_aggregate import TestAggregate
from src.protocol.client.constants import CLIENT_STARTED
from src.protocol.states.constants import HANDLER_STARTED
from src.protocol.states.handler import Handler
from src.protocol.training.constants import ROUND_START, MODEL_TRAINED
from src.protocol.training.fedml.constants import UPDATE_QUEUED_EVENT
from src.protocol.training.fedml.share_update import ShareUpdate


def register_fed_avg_module(handler: Handler):
    handler.register_reducer(CLIENT_STARTED, InitModelLoader(30))
    handler.register_reducer(HANDLER_STARTED, InitTracking(70))
    handler.register_reducer(ROUND_START, StartTrainingPhase(100))
    handler.register_reducer(MODEL_TRAINED, ShareUpdate(200))
    handler.register_reducer(UPDATE_QUEUED_EVENT, FedAvgStartAgg(100))
    handler.register_reducer(START_SELECTION, AcceptAllUpdates(100))
    handler.register_reducer(UPDATES_SELECTED, Aggregate(100))
    handler.register_reducer(AGGREGATION_DONE, TestAggregate(100))
    handler.register_reducer(AGGREGATE_TEST_DONE, CloseRound(100))
