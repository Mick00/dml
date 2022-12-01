from threading import Thread

from src.daeclust.clusters import ClustersRegistry
from src.daeclust.daecluste_helper import get_strategy
from src.nsclust.constants import CLUSTER_SELECTION, CLUSTER_TEST_COMPLETED
from src.nsclust.nsclust_helpers import CURRENT_CLUSTER_KEY, get_cluster_selection_exp_name, get_cluster_training_exp_name
from src.base.client.client_state_helpers import get_node_id
from src.base.states.event import Event
from src.base.states.handler import Handler
from src.base.states.state import State
from src.base.states.transition import StateTransition
from src.base.training.constants import TRAINING_MODULE
from src.base.training.events import TrainModel
from src.base.training.models.experiment import Experiment
from src.base.training.training_client import TrainingClient
from src.base.training.training_state_helper import get_training_client, get_experiment_tracking


class SelectCluster(Event):
    def __init__(self, round_id: int):
        super(SelectCluster, self).__init__(CLUSTER_SELECTION)
        self.round_id = round_id


class CusterSelectionTestCompleted(Event):
    def __init__(self, round_id: int):
        super(CusterSelectionTestCompleted, self).__init__(CLUSTER_TEST_COMPLETED)
        self.round_id = round_id


def test_model(exp_name: str, round_id: int, clusters: ClustersRegistry, training_client: TrainingClient):
    for cluster_id in clusters.get_ids():
        cluster = clusters.get(cluster_id)
        model = cluster.get_model()
        exp = Experiment(exp_name, cluster_id, round_id, cluster.model_name, model)
        training_client.test_model(exp)


def run_tests(
        exp_name: str,
        round_id: int,
        clusters: ClustersRegistry,
        training_client: TrainingClient,
        handler: Handler
):
    test_model(exp_name, round_id, clusters, training_client)
    handler.queue_event(CusterSelectionTestCompleted(round_id))


class StartClusterSelectionTests(StateTransition):
    def transition(self, event: SelectCluster, state: State, handler: Handler):
        strategy = get_strategy(state).for_round(event.round_id - 1)
        training_client = get_training_client(state)
        exp_name = get_cluster_selection_exp_name(state)
        thread = Thread(target=run_tests,
                        args=(exp_name, event.round_id, strategy.clusters, training_client, handler))
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
        strategy = get_strategy(state).for_round(event.round_id - 1)
        cluster = strategy.clusters.get(cluster_id)
        model = cluster.get_model()
        exp = Experiment(get_cluster_training_exp_name(state), cluster_id, event.round_id, cluster.model_name, model)
        handler.queue_event(TrainModel(exp))
