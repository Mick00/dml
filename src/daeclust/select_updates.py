from threading import Thread

from src.daeclust.daeclust_helpers import get_model_loader, get_current_cluster
from src.daeclust.events import SelectedUpdates
from src.daeclust.start_selection import StartUpdateSelection
from src.protocol.client.client_state_helpers import get_node_id
from src.protocol.states.event import Event
from src.protocol.states.handler import Handler
from src.protocol.states.state import State
from src.protocol.states.transition import StateTransition
from src.protocol.training.constants import TRAINING_MODULE
from src.protocol.training.fedml.fedml_state_helper import get_update_queue
from src.protocol.training.fedml.model_update_meta import ModelUpdateMeta, load_update
from src.protocol.training.training_client import TrainingClient
from src.protocol.training.training_state_helper import get_training_client, get_experiment_tracking

SELECTION_TEST_DONE = "training.clustering.test.done"


class DoneSelectionTest(Event):
    def __init__(self, round_id: int, tested_updates:[ModelUpdateMeta]):
        super(DoneSelectionTest, self).__init__(SELECTION_TEST_DONE)
        self.round_id = round_id
        self.tested_updates = tested_updates


def test_updates(cluster_id: str, update_queue: [ModelUpdateMeta], training_client: TrainingClient) -> [ModelUpdateMeta]:
    tested_updates = []
    for update in update_queue:
        if update.cluster_id == cluster_id:
            tested_updates.append(update)
            model = load_update(update)
            training_client.test_model(model)
    return tested_updates


def run_selection(
        handler: Handler,
        training_client: TrainingClient,
        round_id: int,
        cluster_id: str,
        update_queue: [ModelUpdateMeta]
):
    tested_updates = test_updates(cluster_id, update_queue, training_client)
    handler.queue_event(SelectedUpdates(round_id, tested_updates))


class AcceptAllUpdates(StateTransition):

    def transition(self, event: StartUpdateSelection, state: State, handler: Handler):
        update_queue = get_update_queue(state).get_queue(event.round_id)
        handler.queue_event(SelectedUpdates(event.round_id, update_queue))
        # We select all updates all the time
        """
        if event.round_id == 0:
            handler.queue_event(SelectedUpdates(event.round_id, update_queue))
        else:
            cluster_id = get_current_cluster(state)
            thread = Thread(target=run_selection, args=(handler, get_training_client(state), event.round_id, cluster_id, update_queue))
            thread.setName(f"test-round-{event.round_id}")
            thread.start()
            state.update_module(TRAINING_MODULE, {
                "test_thread": thread
            })
        """


class SelectBestPerformingUpdates(StateTransition):
    def transition(self, event: DoneSelectionTest, state: State, handler: Handler):
        exp_tracking = get_experiment_tracking(state)
        my_id = get_node_id(state)
        runs = []


class SelectUpdatesCleanup(StateTransition):
    def transition(self, event: SelectedUpdates, state: State, handler: Handler):
        state.update_module(TRAINING_MODULE, {
            "test_thread": None
        })