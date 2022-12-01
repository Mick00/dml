from threading import Thread

from src.nsclust.events import AggregationCompleted
from src.nsclust.nsclust_helpers import get_model_loader
from src.nsclust.storage.model_loader import ModelLoader
from src.fed_avg.constant import GLOBAL_CLUSTER_ID
from src.fed_avg.events import AggregateModelTestDone
from src.base.config.config_state_helper import get_experience_name
from src.base.logging.log_handler import LogInfo
from src.base.logging.log_training import exp_to_log_dict
from src.base.logging.logging_helpers import get_logger
from src.base.states.event import Event
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.states.event_handler import EventHandlerSimple
from src.base.training.constants import TRAINING_MODULE, EXPERIMENT_TEST, EXPERIMENT_TESTED
from src.base.training.training_client import TrainingClient
from src.base.training.training_state_helper import get_training_client


def run_tests(
        exp_name: str,
        round_id: int,
        model_loader: ModelLoader,
        training_client: TrainingClient,
        handler: EventListener
):
    exp = model_loader.get_experiment(GLOBAL_CLUSTER_ID, round_id + 1, exp_name=exp_name)
    handler.queue_event(LogInfo(EXPERIMENT_TEST, extra=exp_to_log_dict(exp)))
    training_client.test_model(exp)
    handler.queue_event(LogInfo(EXPERIMENT_TESTED, extra=exp_to_log_dict(exp)))
    handler.queue_event(AggregateModelTestDone(round_id))


class TestAggregate(EventHandlerSimple):
    def transition(self, event: AggregationCompleted, state: State, handler: EventListener):
        get_logger(state).info("aggregation.test", extra={"round_id": event.round_id})
        model_loader = get_model_loader(state)
        training_client = get_training_client(state)
        exp_name = get_experience_name(state)
        thread = Thread(target=run_tests,
                        args=(exp_name, event.round_id, model_loader, training_client, handler))
        thread.setName(f"test-clusters-round-{event.round_id}")
        thread.start()
        state.update_module(TRAINING_MODULE, {
            "test-clusters": thread
        })
