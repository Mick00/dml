import pytorch_lightning as pl

from src.base.config.config_state_helper import get_output_path
from src.base.states.event import Event
from src.base.states.state import State
from src.base.states.event_handler import EventHandler, Handler
from src.base.training.models.storage.cluster import Cluster
from src.base.training.constants import TRAINING_MODULE
from src.base.training.models.storage.round import Round


class InitModelLoader(EventHandler):
    def transition(self, event: Event, state: State, handler: Handler):
        model_loader = ModelLoader(get_output_path(state))
        state.get_module_state(TRAINING_MODULE).update({
            "model_loader": model_loader
        })


class ModelLoader:

    clusters: dict[str, Cluster]

    def __init__(self, save_path: str):
        self.save_path = save_path
        self.clusters = {}

    def get_cluster(self, cluster_id: str) -> Cluster:
        if cluster_id in self.clusters:
            return self.clusters.get(cluster_id)
        cluster = Cluster(cluster_id, self.save_path)
        self.clusters[cluster_id] = cluster
        return cluster

    def get_model(self, cluster_id: str, round_id: int) -> pl.LightningModule:
        cluster = self.get_cluster(cluster_id)
        if cluster.round_exists(round_id):
            return cluster.get_round(round_id).get_start_model()
        elif cluster.round_exists(round_id - 1):
            prev_round = cluster.get_round(round_id - 1)
            model = prev_round.get_final_model()
            round = cluster.init_round(round_id, prev_round.model_name)
            round.start_model = prev_round.final_model
            return model

    def set_cluster_genesis(self, cluster_id: str, model_name: str, genesis_state: str, round_id = 0) -> Round:
        cluster = self.get_cluster(cluster_id)
        if cluster.already_initialized():
            raise Exception("Cannot set genesis again")
        cluster.init_storate()
        round = cluster.init_round(round_id, model_name)
        round.start_model = genesis_state
        return round
