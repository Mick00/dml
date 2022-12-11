from threading import Thread

from src.base.client.actions.send import Send
from src.base.states.event import Event
from src.base.states.event_handler import EventHandler
from src.base.states.event_listener import EventListener
from src.base.states.state import State
from src.base.training.constants import MODEL_TRAINED, TRAINING_MODULE
from src.base.training.events import ModelTrained
from src.base.training.models.experiment import Experiment
from src.base.training.training_client import TrainingClient
from src.base.training.training_state_helper import get_training_client
from src.daeclust.clusters import Cluster
from src.daeclust.constants import FLUSH_UPDATES
from src.daeclust.daecluste_helper import get_strategy
from src.daeclust.state.events import SelectedClusters, UpdatedClusters
from src.nsclust.nsclust_helpers import get_cluster_training_exp_name


class FlushUpdates(Event):
    def __init__(self, round_id: int):
        super(FlushUpdates, self).__init__(FLUSH_UPDATES)
        self.round_id = round_id


def train(exp_name: str, clusters: [Cluster], training_client: TrainingClient, el: EventListener):
    round_id = clusters[0].round_id + 1
    for cluster in clusters:
        model = cluster.get_model()
        exp = Experiment(exp_name, cluster.cluster_id, round_id, cluster.model_name, model)
        training_client.train_model(exp)
        exp.model = None  # Removing pointer to model, saved to checkpoint_uri
        el.queue_event(ModelTrained(exp))
    el.queue_event(FlushUpdates(round_id))


class SelectedClustersHandler(EventHandler):
    def _transition(self, event: SelectedClusters, state: State, handler: EventListener) -> [dict]:
        train_clusters = []
        for cluster_id in event.ids:
            strategy = get_strategy(state).for_round(event.round_id - 1)
            cluster = strategy.clusters.get(cluster_id)
            train_clusters.append(cluster)
        exp_name = get_cluster_training_exp_name(state)
        training_client = get_training_client(state)
        thread = Thread(target=train,
                        args=(exp_name, train_clusters, training_client, handler))
        thread.setName(f"train-clusters-round-{event.round_id}")
        thread.start()
        state.update_module(TRAINING_MODULE, {
            "train-clusters": thread
        })


class ModelTrainedBuffer(EventHandler):
    def __init__(self, priority):
        super().__init__(priority)
        self.buffers = {}

    def _transition(self, event: Event, state: State, handler: EventListener) -> [dict]:
        log_app = None
        log_flush = None
        if event.type == MODEL_TRAINED:
            log_app = self.append(event)
            if event.exp.round_id == 0:
                #The genesis round only trains one model
                log_flush = self.flush(0, handler)
        if event.type == FLUSH_UPDATES:
            log_flush = self.flush(event.round_id, handler)
        return [log_app, log_flush]

    def get_buffer(self, round_id):
        if not round_id in self.buffers:
            self.buffers[round_id] = []
        return self.buffers.get(round_id)

    def empty_buffer(self, round_id):
        buffer = self.get_buffer(round_id)
        self.buffers[round_id] = []
        return buffer

    def append(self, event: ModelTrained):
        update = {
                "cluster_id": event.exp.cluster_id,
                "round_id": event.exp.round_id,
                "model_name": event.exp.model_name,
                "checkpoint_uri": event.exp.checkpoint_uri
            }
        self.get_buffer(event.exp.round_id).append(update)
        return self.log_info("model_trained_buffer.appended", extra=update)

    def flush(self, round_id: int, el: EventListener):
        updates = self.empty_buffer(round_id)
        if len(updates) > 0:
            event = UpdatedClusters(updates)
            el.queue_event(event)
            el.queue_event(Send(event))
            return self.log_info("model_trained_buffer.flushed", extra={"n_updates": len(updates), "round_id": round_id})
        else:
            return self.log_warn("model_trained_buffer.flushed.empty", extra={"round_id": round_id})
