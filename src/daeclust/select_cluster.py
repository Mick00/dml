from threading import Thread

from src.daeclust.constants import CLUSTER_SELECTION, CLUSTER_TEST_COMPLETED
from src.daeclust.daeclust_helpers import get_model_loader, CURRENT_CLUSTER_KEY, get_cluster_selection_exp_name, \
    get_cluster_training_exp_name
from src.daeclust.storage.model_loader import ModelLoader
from src.protocol.client.client_state_helpers import get_node_id
from src.protocol.states.event import Event
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition
from src.protocol.training.constants import TRAINING_MODULE
from src.protocol.training.events import TrainModel
from src.protocol.training.fedml.fedml_state_helper import get_update_queue
from src.protocol.training.fedml.model_update_meta import ModelUpdateMeta
from src.protocol.training.training_client import TrainingClient
from src.protocol.training.training_state_helper import get_training_client, get_experiment_tracking


class SelectCluster(Event):
    def __init__(self, round_id: int):
        super(SelectCluster, self).__init__(CLUSTER_SELECTION)
        self.round_id = round_id


class CusterSelectionTestCompleted(Event):
    def __init__(self, round_id: int):
        super(CusterSelectionTestCompleted, self).__init__(CLUSTER_TEST_COMPLETED)
        self.round_id = round_id


def test_model(exp_name: str, round_id: int, clusters: [str], model_loader: ModelLoader, training_client: TrainingClient):
    for cluster_id in clusters:
        exp = model_loader.get_experiment(cluster_id, round_id, exp_name=exp_name)
        training_client.test_model(exp)


def run_tests(
        exp_name: str,
        round_id: int,
        clusters: [str],
        model_loader: ModelLoader,
        training_client: TrainingClient,
        handler: Handler
):
    test_model(exp_name, round_id, clusters, model_loader, training_client)
    handler.queue_event(CusterSelectionTestCompleted(round_id))


class StartClusterSelectionTests(StateTransition):
    def transition(self, event: SelectCluster, state: State, handler: Handler):
        updates_queue = get_update_queue(state)
        active_clusters = updates_queue.get_unique_clusters(event.round_id - 1)
        model_loader = get_model_loader(state)
        training_client = get_training_client(state)
        exp_name = get_cluster_selection_exp_name(state)
        thread = Thread(target=run_tests,
                        args=(exp_name, event.round_id, active_clusters, model_loader, training_client, handler))
        thread.setName(f"test-clusters-round-{event.round_id}")
        thread.start()
        state.update_module(TRAINING_MODULE, {
            "test-clusters": thread
        })


class SelectBestCluster(StateTransition):
    def transition(self, event: CusterSelectionTestCompleted, state: State, handler: Handler):
        exp_tracking = get_experiment_tracking(state)
        my_id = get_node_id(state)
        runs = exp_tracking.search(
            get_cluster_selection_exp_name(state),
            trainer_id=my_id,
            test=True,
            round_id=event.round_id
        )
        best_run = runs[0]
        for run in runs[1:]:
            if run.data.metrics.get('test_loss') < best_run.data.metrics.get('test_loss'):
                best_run = run
        cluster_id = best_run.data.tags.get('cluster_id')
        state.update_module(TRAINING_MODULE, {
            CURRENT_CLUSTER_KEY: cluster_id
        })
        model_loader = get_model_loader(state)
        exp = model_loader.get_experiment(cluster_id, event.round_id, exp_name=get_cluster_training_exp_name(state))
        handler.queue_event(TrainModel(exp))


