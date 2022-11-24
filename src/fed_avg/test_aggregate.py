from threading import Thread

from src.nsclust.nsclust_helpers import get_model_loader
from src.nsclust.storage.model_loader import ModelLoader
from src.fed_avg.constant import GLOBAL_CLUSTER_ID
from src.fed_avg.events import AggregateModelTestDone
from src.protocol.config.config_state_helper import get_experience_name
from src.protocol.states.event import Event
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition
from src.protocol.training.constants import TRAINING_MODULE
from src.protocol.training.training_client import TrainingClient
from src.protocol.training.training_state_helper import get_training_client


def run_tests(
        exp_name: str,
        round_id: int,
        model_loader: ModelLoader,
        training_client: TrainingClient,
        handler: Handler
):
    exp = model_loader.get_experiment(GLOBAL_CLUSTER_ID, round_id + 1, exp_name=exp_name)
    training_client.test_model(exp)
    handler.queue_event(AggregateModelTestDone(round_id))


class TestAggregate(StateTransition):
    def transition(self, event: Event, state: State, handler: Handler):
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
