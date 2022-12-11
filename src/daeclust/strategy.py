import hashlib

from src.base.training.fedml.model_update_meta import ModelUpdateMeta
from src.daeclust.clusters import ClustersRegistry, Cluster
from src.daeclust.update_pool import UpdatePools


def compute_cluster_id(parent_id: str, updates_trainer: [str]) -> str:
    updates_trainer.sort()
    hash_value = parent_id + "".join(updates_trainer)
    return hashlib.sha256(hash_value.encode()).hexdigest()


class RoundStrategy:
    def __init__(self, round_id: int):
        self.update_pools = UpdatePools(round_id)
        self.clusters = ClustersRegistry()


class AggregationStrategy:

    def __init__(self, save_path: str, default_model: str):
        self.rounds = {}
        self.save_path = save_path
        self.default_model = default_model

    def init_round(self, round_id: int):
        round = RoundStrategy(round_id)
        self.rounds[round_id] = round
        return round

    def for_round(self, round_id: int) -> RoundStrategy:
        return self.rounds.get(round_id)

    def round_exists(self, round_id: int) -> bool:
        return round_id in self.rounds

    def add_cluster(self, round_id: int, parent_cluster_id: str, selected_trainers: [str]) -> str:
        updates_pool = self.for_round(round_id).update_pools.for_cluster(parent_cluster_id)
        model_name = updates_pool[0].model_name
        cluster_id = compute_cluster_id(parent_cluster_id, selected_trainers)
        selected_updates = filter(lambda update: update.from_id in selected_trainers, updates_pool)
        updates_path = list(map(lambda update: update.checkpoint_uri, selected_updates))
        new_cluster = Cluster(cluster_id, model_name, round_id, self.save_path, updates_path)
        self.for_round(round_id).clusters.add(cluster_id, new_cluster)
        return cluster_id

    def add_update(self, update_meta: ModelUpdateMeta):
        self.for_round(update_meta.round_id).update_pools.add_update(update_meta)